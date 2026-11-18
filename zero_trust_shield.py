import os
import time
import hmac
import hashlib
import sqlite3
import logging
from functools import wraps
from collections import defaultdict
from flask import request, jsonify, g

# إعداد سجل التدقيق الأمني غير القابل للتلاعب
logging.basicConfig(
    filename="security_audit_immutable.log",
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s"
)

# مفاتيح العزل الصارم (تُقرأ حصراً من متغيرات البيئة ولا تُكتب في الكود أبداً)
MASTER_KILL_SWITCH = os.getenv("OMNIVERSE_EMERGENCY_LOCKDOWN", "false").lower() == "true"
SOVEREIGN_HMAC_SECRET = os.getenv("SOVEREIGN_HMAC_SECRET", "").encode("utf-8")

# حدود المعدل الديناميكية ضد هجمات الذكاء الاصطناعي المؤتمتة (Rate Limiting)
RATE_LIMIT_WINDOW = 60  # ثانية
MAX_REQUESTS_PER_IP = 30
MAX_LYO_TX_PER_USER = 5
ip_request_log = defaultdict(list)
user_tx_log = defaultdict(list)

# سقف الحماية المالية التلقائي لكل عملية LYO (Circuit Breaker)
MAX_SINGLE_LYO_AMOUNT = float(os.getenv("MAX_SINGLE_LYO_AMOUNT", "500.0"))


def _clean_old_timestamps(records, window):
    now = time.time()
    return [t for t in records if now - t < window]


def log_security_event(event_type, actor_id, details, severity="WARNING"):
    ip = request.headers.get("X-Forwarded-For", request.remote_addr)
    entry = f"EVENT={event_type} | ACTOR={actor_id} | IP={ip} | PATH={request.path} | DETAILS={details}"
    if severity == "CRITICAL":
        logging.critical(entry)
    else:
        logging.warning(entry)


def verify_hmac_signature(payload_bytes, provided_signature):
    """التحقق التشفيري من سلامة الطلب وعدم تعديله أثناء النقل"""
    if not SOVEREIGN_HMAC_SECRET or not provided_signature:
        return False
    expected = hmac.new(SOVEREIGN_HMAC_SECRET, payload_bytes, hashlib.sha256).hexdigest()
    return hmac.compare_digest(expected, provided_signature)


def sovereign_zero_trust_guard(require_kyc=True, is_lyo_financial=False, require_sovereign_sig=False):
    """
    حارس الثقة الصفرية الشامل لمنظومة أومنيفيرس وعقدة طرابلس
    """
    def decorator(f):
        @wraps(f)
        def wrapped(*args, **kwargs):
            # 1. مفتاح الإغلاق السيادي الفوري عند رصد هجوم واسع
            if MASTER_KILL_SWITCH:
                log_security_event("EMERGENCY_LOCKDOWN_BLOCK", "SYSTEM", "Blocked during lockdown", "CRITICAL")
                return jsonify({"status": "locked", "error": "System in sovereign maintenance lockdown"}), 503

            ip = request.headers.get("X-Forwarded-For", request.remote_addr)
            now = time.time()

            # 2. صد هجمات الفحص والاستنزاف الآلي بالذكاء الاصطناعي (IP Rate Limiting)
            ip_request_log[ip] = _clean_old_timestamps(ip_request_log[ip], RATE_LIMIT_WINDOW)
            if len(ip_request_log[ip]) >= MAX_REQUESTS_PER_IP:
                log_security_event("AI_FLOOD_DETECTED", "ANONYMOUS", f"Exceeded {MAX_REQUESTS_PER_IP} req/min")
                return jsonify({"error": "Rate limit exceeded. Automated behavior blocked."}), 429
            ip_request_log[ip].append(now)

            # 3. التحقق من هوية مستخدم Pi وامتثاله لـ KYC (توافقاً مع سياسات شبكة باي)
            pi_uid = request.headers.get("X-Pi-UID")
            kyc_verified = request.headers.get("X-Pi-KYC-Verified", "false").lower() == "true"

            if require_kyc:
                if not pi_uid or not kyc_verified:
                    log_security_event("UNVERIFIED_PI_ACCESS", pi_uid or "NONE", "Missing Pi UID or KYC")
                    return jsonify({"error": "Pi Network KYC verification required"}), 403

            # 4. التحقق التشفيري من التوقيع للعمليات السيادية أو حركة الوكلاء الحساسة
            if require_sovereign_sig:
                sig = request.headers.get("X-Sovereign-Signature", "")
                if not verify_hmac_signature(request.get_data(), sig):
                    log_security_event("INVALID_HMAC_SIGNATURE", pi_uid or "UNKNOWN", "Tampered or unsigned payload", "CRITICAL")
                    return jsonify({"error": "Invalid cryptographic signature"}), 401

            # 5. قاطع الدائرة المالي لحماية عملة LYO من الاستنزاف الآلي
            if is_lyo_financial:
                user_tx_log[pi_uid] = _clean_old_timestamps(user_tx_log[pi_uid], RATE_LIMIT_WINDOW)
                if len(user_tx_log[pi_uid]) >= MAX_LYO_TX_PER_USER:
                    log_security_event("LYO_VELOCITY_BREACH", pi_uid, "Too many LYO transactions/min", "CRITICAL")
                    return jsonify({"error": "Transaction velocity limit exceeded"}), 429

                data = request.get_json(silent=True) or {}
                amount = float(data.get("amount", 0))
                if amount <= 0 or amount > MAX_SINGLE_LYO_AMOUNT:
                    log_security_event("LYO_CIRCUIT_BREAKER", pi_uid, f"Blocked abnormal amount: {amount}", "CRITICAL")
                    return jsonify({"error": f"Amount violates single-transaction safety cap ({MAX_SINGLE_LYO_AMOUNT} LYO)"}), 400

                user_tx_log[pi_uid].append(now)

            g.verified_pi_uid = pi_uid
            return f(*args, **kwargs)
        return wrapped
    return decorator