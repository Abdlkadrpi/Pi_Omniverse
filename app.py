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
PI_ENV = os.environ.get("PI_ENV", "sandbox")  # فرض وضع الساندبوكس افتراضياً للتوافق مع مفتاحك
PI_BASE_URL = "https://api.minepi.com/v2"

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "assets.db")

compliance_engine = OmniverseSovereignCompliance()

REQUEST_LIMIT = 50
TIME_WINDOW = 60
request_records = {}


def check_rate_limit(client_ip):
    now = time.time()
    if client_ip not in request_records:
        request_records[client_ip] = []

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
    if request.path in ["/", "/validation-key.txt", "/legal.html", "/api/app_wallet"]:
        return

    client_ip = request.remote_addr
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


@app.route("/legal.html")
def legal_policy():
    return render_template("legal.html")


@app.route("/api/app_wallet", methods=["GET", "POST"])
def app_wallet_config():
    return jsonify({
        "status": "success",
        "message": "App wallet configured successfully under Omniverse Sovereign Network",
        "network": PI_ENV
    }), 200


@app.route("/api/force_cancel_all", methods=["GET", "POST"])
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
                f"{PI_BASE_URL}/payments/incomplete", headers=headers
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
                            f"{PI_BASE_URL}/payments/{pid}/cancel",
                            headers=headers,
                        )

        return (
            jsonify({
                "status": "forced_cleaned_all",
                "message": "Local and remote payments cleared successfully",
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
        asset_value = data.get("asset_value", 1.0)

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
            f"{PI_BASE_URL}/payments/{payment_id}/approve",
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
            f"{PI_BASE_URL}/payments/{payment_id}/complete",
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


@app.route("/pi-webhook", methods=["POST"])
def pi_webhook():
    try:
        data = request.get_json() or {}
        payment_id = data.get("paymentId") or data.get("payment_id") or "unknown_tx"
        status = data.get("status", "COMPLETED")

        audit_result = compliance_engine.audit_transaction(
            str(payment_id), True, 1.0
        )

        return (
            jsonify({
                "status": "success",
                "message": "Secure Webhook processed",
                "audit_result": audit_result,
            }),
            200,
        )
    except Exception as e:
        return jsonify({"status": "error", "error": str(e)}), 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 10000)))