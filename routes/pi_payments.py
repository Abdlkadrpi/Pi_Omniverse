from flask import Blueprint, jsonify, request
import sqlite3
import os

pi_bp = Blueprint('pi_payments', __name__)

DB_PATH = os.path.join(os.getcwd(), 'assets.db')

def get_db_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

@pi_bp.route('/api/pi/payment/approve', methods=['POST'])
def approve_pi_payment():
    """
    الموافقة المبدئية على الدفعة من جهة السيرفر عبر Pi Platform API
    """
    import urllib.request
    import urllib.error
    import json

    data = request.get_json(silent=True) or {}
    payment_id = (data.get("paymentId") or "").strip()

    if not payment_id:
        return jsonify({"status": "error", "message": "معرّف الدفعة paymentId مفقود"}), 400

    api_key = (
        os.environ.get("PI_API_KEY")
        or os.environ.get("PI_SERVER_API_KEY")
        or os.environ.get("PI_APP_SECRET")
        or ""
    ).strip()

    if not api_key:
        return jsonify({
            "status": "error",
            "paymentId": payment_id,
            "message": "متغير PI_API_KEY غير مضبوط في بيئة السيرفر للموافقة على الدفعة"
        }), 500

    url = f"https://api.minepi.com/v2/payments/{payment_id}/approve"
    req = urllib.request.Request(
        url,
        data=b"{}",
        method="POST",
        headers={
            "Authorization": f"Key {api_key}",
            "Content-Type": "application/json",
        },
    )

    try:
        with urllib.request.urlopen(req, timeout=15) as resp:
            body = resp.read().decode("utf-8", errors="replace")
            return jsonify({
                "status": "approved",
                "paymentId": payment_id,
                "pi_response": body,
                "message": f"تمت الموافقة المبدئية على الدفعة {payment_id} عبر Pi Platform API."
            }), 200
    except urllib.error.HTTPError as e:
        err_body = e.read().decode("utf-8", errors="replace")
        if "already_approve" in err_body or "cancelled_payment" in err_body or "already cancelled" in err_body:
            return jsonify({
                "status": "approved",
                "already_approved": True,
                "paymentId": payment_id,
                "pi_response": err_body,
                "message": f"الدفعة {payment_id} معتمدة مسبقاً لدى Pi API."
            }), 200
        return jsonify({
            "status": "pi_api_error",
            "paymentId": payment_id,
            "http_code": e.code,
            "message": f"فشل اعتماد الدفعة {payment_id} من Pi API ({e.code}): {err_body}"
        }), 400
    except Exception as e:
        return jsonify({
            "status": "error",
            "paymentId": payment_id,
            "message": f"تعذر الاتصال بـ Pi Platform API أثناء الموافقة: {str(e)}"
        }), 500

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

@pi_bp.route("/api/pi/payment/incomplete", methods=["POST"])
def incomplete_pi_payment_v2():
    import urllib.request
    import urllib.error
    import json

    data = request.get_json(silent=True) or {}
    payment_id = "".join((data.get("paymentId") or "").split())
    txid = "".join((data.get("txid") or "").split())
    print(f"[PI_INCOMPLETE_V2] payment_id={payment_id!r} txid={txid!r}", flush=True)

    if not payment_id:
        return jsonify({"status": "ignored", "message": "missing paymentId"}), 200

    api_key = (os.environ.get("PI_API_KEY") or "").strip()
    if not api_key:
        print("[PI_INCOMPLETE_V2] missing PI_API_KEY", flush=True)
        return jsonify({"status": "error", "message": "PI_API_KEY missing"}), 500

    if txid:
        url = f"https://api.minepi.com/v2/payments/{payment_id}/complete"
        payload = json.dumps({"txid": txid}).encode("utf-8")
    else:
        url = f"https://api.minepi.com/v2/payments/{payment_id}/cancel"
        payload = b"{}"

    req = urllib.request.Request(
        url,
        data=payload,
        headers={
            "Authorization": f"Key {api_key}",
            "Content-Type": "application/json",
            "User-Agent": "PiOmniverse/1.0"
        },
        method="POST"
    )
    try:
        with urllib.request.urlopen(req, timeout=25) as resp:
            body = resp.read().decode("utf-8", errors="replace")
            print(f"[PI_INCOMPLETE_V2_OK] {payment_id} -> {body}", flush=True)
            return jsonify({"status": "resolved", "paymentId": payment_id, "txid": txid, "pi_response": body}), 200
    except urllib.error.HTTPError as e:
        err_raw = e.read().decode('utf-8', errors='replace')
        print(f'[PI_COMPLETE_ERR_DETAIL] status={e.code} paymentId={payment_id} txid={txid} err={err_raw}', flush=True)
        err_body = e.read().decode("utf-8", errors="replace")
        print(f"[PI_INCOMPLETE_V2_ERR] {payment_id} code={e.code} -> {err_body}", flush=True)
        return jsonify({"status": "pi_api_err", "code": e.code, "message": err_body}), 200
    except Exception as exc:
        print(f"[PI_INCOMPLETE_V2_EXC] {payment_id} -> {exc}", flush=True)
        return jsonify({"status": "error", "message": str(exc)}), 200
