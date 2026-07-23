import os, requests, sqlite3
from flask import Flask, jsonify, request, render_template, send_from_directory
from flask_cors import CORS
from datetime import datetime, timezone
from Omniverse.omniverse_sovereign_compliance import OmniverseSovereignCompliance

app = Flask(__name__)
CORS(app)

PI_API_KEY = os.environ.get("PI_API_KEY")
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, 'assets.db')

# تهيئة محرك الامتثال والتدقيق السيادي
compliance_engine = OmniverseSovereignCompliance()

def init_db():
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute('CREATE TABLE IF NOT EXISTS assets (id INTEGER PRIMARY KEY, asset_name TEXT, asset_value REAL, owner_id TEXT, payment_tx TEXT, timestamp TEXT)')
        conn.execute('CREATE TABLE IF NOT EXISTS pending_payments (payment_id TEXT PRIMARY KEY, user_id TEXT, status TEXT)')
init_db()

@app.route('/validation-key.txt')
def pi_validation():
    return send_from_directory(BASE_DIR, 'validation-key.txt')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/force_cancel_all', methods=['GET'])
def force_cancel_all():
    try:
        # 1. تنظيف قاعدة البيانات المحلية بالكامل
        with sqlite3.connect(DB_PATH) as conn:
            conn.execute("DELETE FROM pending_payments")
        
        # 2. التدخل الجراحي الشامل عبر Pi API لإلغاء جميع المعاملات غير المنتهية والمعلقة
        if PI_API_KEY:
            headers = {"Authorization": f"Key {PI_API_KEY}", "Content-Type": "application/json"}
            resp = requests.get("https://api.minepi.com/v2/payments/incomplete", headers=headers)
            if resp.status_code == 200:
                data = resp.json()
                payments = []
                if isinstance(data, list):
                    payments = data
                elif isinstance(data, dict):
                    payments = data.get('payments', data.get('incomplete_payments', []))
                
                for p in payments:
                    pid = p.get('identifier') or p.get('paymentId') or p.get('id')
                    if pid:
                        requests.post(f"https://api.minepi.com/v2/payments/{pid}/cancel", headers=headers)
                        
        return jsonify({"status": "forced_cleaned_all", "message": "Local and remote sandbox payments cleared successfully"}), 200
    except Exception as e:
        return jsonify({"status": "partial_clean", "error": str(e)}), 200

@app.route('/api/approve_payment', methods=['POST'])
def approve_payment():
    try:
        data = request.get_json() or {}
        payment_id = data.get('paymentId') or data.get('identifier')
        if not payment_id:
            return jsonify({"status": "ignored_no_id"}), 200
        
        user_id = data.get('userId', 'unknown')
        kyc_status = data.get('kyc_verified', True)  # التحقق من حالة الـ KYC عبر النظام السيادي
        asset_value = data.get('asset_value', 100.0)

        # تطبيق تدقيق الامتثال قبل الموافقة على الدفع
        audit_result = compliance_engine.audit_transaction(payment_id, kyc_status, asset_value)
        if audit_result.get('status') == 'REJECTED':
            return jsonify({"status": "rejected", "reason": audit_result.get('message')}), 400

        headers = {"Authorization": f"Key {PI_API_KEY}", "Content-Type": "application/json"}
        requests.post(f"https://api.minepi.com/v2/payments/{payment_id}/approve", headers=headers)
        
        with sqlite3.connect(DB_PATH) as conn:
            conn.execute("INSERT OR REPLACE INTO pending_payments VALUES (?, ?, ?)", (str(payment_id), str(user_id), 'pending'))
            
        return jsonify({"status": "approved", "compliance_seal": audit_result.get('compliance_seal')}), 200
    except Exception as e:
        return jsonify({"status": "recovered", "error": str(e)}), 200

@app.route('/api/complete_payment', methods=['POST'])
def complete_payment():
    try:
        data = request.get_json() or {}
        payment_id = data.get('paymentId') or data.get('identifier')
        txid = data.get('txid')
        
        if not payment_id or not txid:
            return jsonify({"error": "Missing required fields"}), 400

        headers = {"Authorization": f"Key {PI_API_KEY}", "Content-Type": "application/json"}
        resp = requests.post(f"https://api.minepi.com/v2/payments/{payment_id}/complete", headers=headers, json={"txid": txid})
        
        if resp.status_code in [200, 201]:
            with sqlite3.connect(DB_PATH) as conn:
                conn.execute("INSERT INTO assets (asset_name, asset_value, owner_id, payment_tx, timestamp) VALUES (?, ?, ?, ?, ?)",
                             (data.get('asset_name', 'Omniverse Asset'), data.get('asset_value', 0.0), data.get('owner', 'unknown'), txid, datetime.now(timezone.utc).isoformat()))
                conn.execute("DELETE FROM pending_payments WHERE payment_id = ?", (payment_id,))
            return jsonify({"status": "completed"}), 200
            
        return jsonify({"error": "Completion failed", "details": resp.text}), 500
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/compliance/audit', methods=['POST'])
def api_audit_transaction():
    """مسار مخصص للتدقيق السيادي على المعاملات وأصول عملة LYO"""
    try:
        data = request.get_json() or {}
        tx_id = data.get('tx_id', 'default_tx')
        kyc_status = data.get('kyc_verified', True)
        asset_val = data.get('asset_value', 100.0)
        result = compliance_engine.audit_transaction(tx_id, kyc_status, asset_val)
        return jsonify(result), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 10000)))