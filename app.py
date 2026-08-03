from datetime import datetime, timezone
import os
from Omniverse.omniverse_sovereign_compliance import OmniverseSovereignCompliance
from flask import Flask, jsonify, render_template, request, send_from_directory
from flask_cors import CORS
import requests
import sqlite3
import time

app = Flask(__name__)
CORS(app)

PI_API_KEY = os.environ.get("PI_API_KEY")
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "assets.db")

# تهيئة محرك الامتثال والتدقيق السيادي
compliance_engine = OmniverseSovereignCompliance()

# نظام حماية بسيط للحد من معدل الطلبات (Rate Limiting) لمنع هجمات الاستنزاف
REQUEST_LIMIT = 30  # أقصى عدد طلبات مسموح به
TIME_WINDOW = 60  # خلال 60 ثانية
request_records = {}


def check_rate_limit(client_ip):
  now = time.time()
  if client_ip not in request_records:
    request_records[client_ip] = []

  # تنظيف الطلبات القديمة خارج النافذة الزمنية
  request_records[client_ip] = [
      t for t in request_records[client_ip] if now - t < TIME_WINDOW
  ]

  if len(request_records[client_ip]) >= REQUEST_LIMIT:
    return False

  request_records[client_ip].append(now)
  return True


def init_db():
  with sqlite3.connect(DB_PATH) as conn:
    conn.execute(
        "CREATE TABLE IF NOT EXISTS assets (id INTEGER PRIMARY KEY, asset_name"
        " TEXT, asset_value REAL, owner_id TEXT, payment_tx TEXT, timestamp"
        " TEXT)"
    )
    conn.execute(
        "CREATE TABLE IF NOT EXISTS pending_payments (payment_id TEXT PRIMARY"
        " KEY, user_id TEXT, status TEXT)"
    )


init_db()


@app.before_request
def security_firewall():
  # استثناء الصفحة الرئيسية وملف التحقق من قيود الحماية المباشرة
  if request.path in ["/", "/validation-key.txt"]:
    return

  client_ip = request.remote_addr
  # تطبيق حدود معدل الطلبات للأمان
  if not check_rate_limit(client_ip):
    return (
        jsonify({
            "status": "security_block",
            "error": "Rate limit exceeded. Too many requests.",
        }),
        429,
    )


@app.route("/validation-key.txt")
def pi_validation():
  return send_from_directory(BASE_DIR, "validation-key.txt")


@app.route("/")
def index():
  return render_template("index.html")


@app.route("/api/force_cancel_all", methods=["GET"])
def force_cancel_all():
  try:
    with sqlite3.connect(DB_PATH) as conn:
      conn.execute("DELETE FROM pending_payments")

    if PI_API_KEY:
      headers = {
          "Authorization": f"Key {PI_API_KEY}",
          "Content-Type": "application/json",
      }
      resp = requests.get(
          "https://api.minepi.com/v2/payments/incomplete", headers=headers
      )
      if resp.status_code == 200:
        data = resp.json()
        payments = []
        if isinstance(data, list):
          payments = data
        elif isinstance(data, dict):
          payments = data.get(
              "payments", data.get("incomplete_payments", [])
          )

        for p in payments:
          pid = p.get("identifier") or p.get("paymentId") or p.get("id")
          if pid:
            requests.post(
                f"https://api.minepi.com/v2/payments/{pid}/cancel",
                headers=headers,
            )

    return (
        jsonify({
            "status": "forced_cleaned_all",
            "message": (
                "Local and remote sandbox payments cleared successfully under"
                " sovereign security"
            ),
        }),
        200,
    )
  except Exception as e:
    return jsonify({"status": "partial_clean", "error": str(e)}), 200


@app.route("/api/approve_payment", methods=["POST"])
def approve_payment():
  try:
    data = request.get_json() or {}
    payment_id = data.get("paymentId") or data.get("identifier")
    if not payment_id:
      return jsonify({"status": "ignored_no_id"}), 200

    user_id = data.get("userId", "unknown")
    kyc_status = data.get("kyc_verified", True)
    asset_value = data.get("asset_value", 100.0)

    audit_result = compliance_engine.audit_transaction(
        payment_id, kyc_status, asset_value
    )
    if audit_result.get("status") == "REJECTED":
      return (
          jsonify(
              {"status": "rejected", "reason": audit_result.get("message")}
          ),
          400,
      )

    headers = {
        "Authorization": f"Key {PI_API_KEY}",
        "Content-Type": "application/json",
    }
    requests.post(
        f"https://api.minepi.com/v2/payments/{payment_id}/approve",
        headers=headers,
    )

    with sqlite3.connect(DB_PATH) as conn:
      conn.execute(
          "INSERT OR REPLACE INTO pending_payments VALUES (?, ?, ?)",
          (str(payment_id), str(user_id), "pending"),
      )

    return (
        jsonify({
            "status": "approved",
            "compliance_seal": audit_result.get("compliance_seal"),
        }),
        200,
    )
  except Exception as e:
    return jsonify({"status": "recovered", "error": str(e)}), 200


@app.route("/api/complete_payment", methods=["POST"])
def complete_payment():
  try:
    data = request.get_json() or {}
    payment_id = data.get("paymentId") or data.get("identifier")
    txid = data.get("txid")

    if not payment_id or not txid:
      return jsonify({"error": "Missing required fields"}), 400

    headers = {
        "Authorization": f"Key {PI_API_KEY}",
        "Content-Type": "application/json",
    }
    resp = requests.post(
        f"https://api.minepi.com/v2/payments/{payment_id}/complete",
        headers=headers,
        json={"txid": txid},
    )

    if resp.status_code in [200, 201]:
      with sqlite3.connect(DB_PATH) as conn:
        conn.execute(
            "INSERT INTO assets (asset_name, asset_value, owner_id,"
            " payment_tx, timestamp) VALUES (?, ?, ?, ?, ?)",
            (
                data.get("asset_name", "Omniverse Asset"),
                data.get("asset_value", 0.0),
                data.get("owner", "unknown"),
                txid,
                datetime.now(timezone.utc).isoformat(),
            ),
        )
        conn.execute(
            "DELETE FROM pending_payments WHERE payment_id = ?", (payment_id,)
        )
      return jsonify({"status": "completed"}), 200

    return jsonify({"error": "Completion failed", "details": resp.text}), 500
  except Exception as e:
    return jsonify({"error": str(e)}), 500


@app.route("/api/compliance/audit", methods=["POST"])
def api_audit_transaction():
  try:
    data = request.get_json() or {}
    tx_id = data.get("tx_id", "default_tx")
    kyc_status = data.get("kyc_verified", True)
    asset_val = data.get("asset_value", 100.0)
    result = compliance_engine.audit_transaction(tx_id, kyc_status, asset_val)
    return jsonify(result), 200
  except Exception as e:
    return jsonify({"error": str(e)}), 500


@app.route("/pi-webhook", methods=["POST"])
def pi_webhook():
  try:
    data = request.get_json() or {}
    payment_id = data.get("paymentId") or data.get("payment_id") or "unknown_tx"
    user_id = data.get("userId") or data.get("user_uid") or "anonymous"
    status = data.get("status", "COMPLETED")

    # تدقيق وتوثيق المعاملة عبر المحرك السيادي
    # نفترض تمرير قيم افتراضية آمنة للتدقيق إذا لم توفر البيانات بالطلب
    audit_result = compliance_engine.audit_transaction(
        str(payment_id), True, 100.0
    )

    print(
        f"[جدار الحماية السيادي] تم فحص وتوثيق المعاملة بنجاح: {payment_id} -"
        f" الحالة: {status}"
    )

    return (
        jsonify({
            "status": "success",
            "message": "Secure Webhook processed under Sovereign Firewall",
            "audit_result": audit_result,
        }),
        200,
    )
  except Exception as e:
    return jsonify({"status": "error", "error": str(e)}), 500


if __name__ == "__main__":
  app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 10000)))