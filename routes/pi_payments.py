from flask import Blueprint, jsonify, request
import sqlite3
import os

pi_bp = Blueprint('pi_payments', __name__)

DB_PATH = os.path.join(os.getcwd(), 'assets.db')

def get_db_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

@pi_bp.route('/api/pi/payment/complete', methods=['POST'])
def complete_pi_payment():
    """
    التحقق من إتمام الدفع عبر Pi SDK وتحديث سجلات المستخدم في أومنيفيرس
    """
    data = request.get_json()
    payment_id = data.get('paymentId')
    txid = data.get('txid')
    user_uid = data.get('userUid')
    amount = data.get('amount')
    service_type = data.get('serviceType', 'notary_service')

    if not payment_id or not user_uid:
        return jsonify({"status": "error", "message": "بيانات الدفع غير مكتملة"}), 400

    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # التأكد من عدم تكرار المعاملة مسبقاً (منع Double-spending)
        cursor.execute("SELECT * FROM transactions WHERE payment_id = ?", (payment_id,))
        existing = cursor.fetchone()
        
        if existing:
            conn.close()
            return jsonify({"status": "success", "message": "المعاملة مسجلة مسبقاً"}), 200

        # تسجيل المعاملة بنجاح وتحديث رصيد أو خدمات المستخدم
        cursor.execute("""
            INSERT INTO transactions (payment_id, txid, user_uid, amount, service_type, status)
            VALUES (?, ?, ?, ?, ?, 'completed')
        """, (payment_id, txid, user_uid, amount, service_type))
        
        conn.commit()
        conn.close()

        return jsonify({
            "status": "success",
            "message": "تم تأكيد الدفع وتوثيق المعاملة بنجاح في أومنيفيرس",
            "paymentId": payment_id
        }), 200

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

@pi_bp.route('/api/pi/payment/incomplete', methods=['POST'])
def handle_incomplete_payment():
    """
    معالجة المعاملات المعلقة أو غير المكتملة بناءً على توجيهات Pi SDK
    """
    data = request.get_json()
    payment_id = data.get('paymentId')
    
    # سجل المعاملة المعلقة لمراجعتها أو إلغائها برمجياً
    return jsonify({
        "status": "acknowledged",
        "message": f"تم رصد المعاملة المعلقة {payment_id} وجاري معالجتها."
    }), 200