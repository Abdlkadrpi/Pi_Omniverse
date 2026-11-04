import time
import re
import logging
from functools import wraps
from flask import request, jsonify

# إنشاء مسجل خاص (Dedicated Logger) للجدار الناري لعدم التداخل مع السجلات العامة
logger = logging.getLogger('OmniverseWAF')
logger.setLevel(logging.INFO)

# التأكد من عدم تكرار الـ Handlers إذا تم إعادة تحميل الملف
if not logger.handlers:
    handler = logging.FileHandler('omniverse_security_audit.log', encoding='utf-8')
    formatter = logging.Formatter('%(asctime)s [%(levelname)s] - Client-IP: %(remote_ip)s - Path: %(path)s - Message: %(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)

class OmniverseSmartWAF:
    def __init__(self, app=None, max_requests_per_minute=60):
        self.app = app
        self.rate_limit_window = 60  # بالثواني
        self.max_requests = max_requests_per_minute
        self.request_records = {}  # لتخزين تتبع الـ IPs
        self.blocked_ips = set()   # قائمة الحظر المؤقت
        
        # أنماط الهجمات والحقن الشائعة (Regex Patterns)
        self.injection_patterns = [
            # SQL Injection patterns
            re.compile(r"(\%27)|(')|(--)|(\/\*)|(\*\/)|(UNION)|(SELECT)|(DROP)|(INSERT)|(UPDATE)|(DELETE)", re.IGNORECASE),
            # Command / System Injection patterns
            re.compile(r"(;|\||&|\$\(|\bcat\b|\bwget\b|\bcurl\b|\bnc\b|\bpython3?\b)", re.IGNORECASE),
            # Prompt Injection / LLM Abuse patterns targeting AI agents
            re.compile(r"(ignore previous instructions|system prompt|disregard all rules|reveal secret key)", re.IGNORECASE)
        ]

        if app is not None:
            self.init_app(app)

    def init_app(self, app):
        @app.before_request
        def inspect_incoming_traffic():
            client_ip = request.remote_addr or "127.0.0.1"
            current_path = request.path

            # 1. التحقق مما إذا كان الـ IP محظوراً
            if client_ip in self.blocked_ips:
                self._log_security_event(client_ip, current_path, "Blocked IP attempted access", level="WARNING")
                return jsonify({
                    "status": "error",
                    "code": 403,
                    "message": "Access denied by Omniverse PRISM Security Supervisor."
                }), 403

            # 2. فحص معدل الطلبات (Rate Limiting & DDoS Prevention)
            if not self._check_rate_limit(client_ip):
                self.blocked_ips.add(client_ip)
                self._log_security_event(client_ip, current_path, "Rate limit exceeded - IP temporarily banned", level="ERROR")
                return jsonify({
                    "status": "error",
                    "code": 429,
                    "message": "Rate limit exceeded. Suspicious traffic pattern detected."
                }), 429

            # 3. فحص محتوى الطلب بحثاً عن محاولات حقن (Payload Inspection)
            threat_detected, payload_detail = self._inspect_payload()
            if threat_detected:
                self._log_security_event(client_ip, current_path, f"Malicious payload detected: {payload_detail}", level="CRITICAL")
                return jsonify({
                    "status": "error",
                    "code": 400,
                    "message": "Request blocked due to security policy violation (Injection Pattern Match)."
                }), 400

    def _check_rate_limit(self, client_ip):
        current_time = time.time()
        if client_ip not in self.request_records:
            self.request_records[client_ip] = []

        # تنظيف السجلات القديمة خارج نافذة الزمن
        self.request_records[client_ip] = [
            t for t in self.request_records[client_ip] 
            if current_time - t < self.rate_limit_window
        ]

        if len(self.request_records[client_ip]) >= self.max_requests:
            return False

        self.request_records[client_ip].append(current_time)
        return True

    def _inspect_payload(self):
        payload_data = ""
        try:
            if request.args:
                payload_data += str(request.args.to_dict())
            if request.is_json and request.get_json(silent=True):
                payload_data += str(request.get_json(silent=True))
            if request.form:
                payload_data += str(request.form.to_dict())
        except Exception as e:
            return True, f"Malformed payload parsing error: {str(e)}"

        for pattern in self.injection_patterns:
            if pattern.search(payload_data):
                return True, pattern.pattern

        return False, None

    def _log_security_event(self, remote_ip, path, message, level="INFO"):
        extra = {'remote_ip': remote_ip, 'path': path}
        if level == "CRITICAL":
            logger.critical(message, extra=extra)
        elif level == "ERROR":
            logger.error(message, extra=extra)
        elif level == "WARNING":
            logger.warning(message, extra=extra)
        else:
            logger.info(message, extra=extra)

# دالة مساعدة لتزيين المسارات الحساسة (Decorator)
def require_prism_clearance(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        auth_header = request.headers.get('X-Omniverse-Auth-Token')
        if not auth_header or not auth_header.startswith('OMN-SEC-'):
            return jsonify({
                "status": "error",
                "code": 401,
                "message": "Unauthorized: PRISM AI Supervisor clearance token missing or invalid."
            }), 401
        return f(*args, **kwargs)
    return decorated_function