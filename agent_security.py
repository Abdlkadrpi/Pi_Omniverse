# agent_security.py
from functools import wraps
from flask import request, jsonify
from crypto_agility import CryptoAgilityEngine

# تفعيل محرك الحماية الكمية والهجينة
engine = CryptoAgilityEngine(mode="quantum_hybrid")

def require_zero_trust_security(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # التقاط ترويسات الأمان (Security Headers)
        client_sig = request.headers.get('X-Quantum-Signature')
        nonce = request.headers.get('X-Request-Nonce')
        user_kyc_status = request.headers.get('X-Pi-KYC-Verified')

        # 1. سياسة شبكة باي والامتثال الدولي: التحقق الإلزامي من مرحلة KYC لاستخدام عملة LYO
        if user_kyc_status != 'true':
            return jsonify({
                "status": "error",
                "compliance_error": "PI_KYC_REQUIRED",
                "message": "Access denied: Pi Network KYC verification is mandatory for LYO utility and agent operations."
            }), 403

        # 2. التحقق من وجود بصمات الأمان والتوقيع الكمي
        if not client_sig or not nonce:
            return jsonify({
                "status": "error",
                "security_error": "ZERO_TRUST_VIOLATION",
                "message": "Security headers missing: Request rejected by Zero-Trust gateway."
            }), 401

        # 3. استخراج الحمولة والتحقق من سلامتها ضد هجمات إعادة التشغيل (Replay Attacks)
        body_data = request.get_data(as_text=True)
        secret_node_key = "OMNIVERSE_SECURE_TRIPOLI_NODE_KEY_2026"  # يُفضل جلبها من متغيرات البيئة في Render
        
        if not engine.verify_signature(secret_node_key, body_data + nonce, client_sig):
            return jsonify({
                "status": "error",
                "crypto_error": "QUANTUM_SIGNATURE_MISMATCH",
                "message": "Cryptographic validation failed. Potential quantum decryption or tampering attempt detected."
            }), 403

        return f(*args, **kwargs)
    return decorated_function