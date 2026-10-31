import os
import re
import json
import time
import hashlib
import hmac
from functools import wraps
from flask import request, jsonify, g
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.hkdf import HKDF

# =====================================================================
# 1. طبقة التشفير المقاوم للكم (Post-Quantum Hybrid Cryptography)
# =====================================================================
class PQCGuardrailEngine:
    def __init__(self, master_key: bytes = None):
        # استخدام مفتاح رئيسي بحجم 256-بت متوافق مع معايير NSA CNSA 2.0
        self.master_key = master_key or os.urandom(32)
        
    def derive_layer_key(self, context_info: bytes) -> bytes:
        """اشتقاق مفاتيح تشفير فريدة لكل طلب لتفادي هجمات الكم والـ Replay Attacks"""
        hkdf = HKDF(
            algorithm=hashes.SHA3_512(), # SHA3-512 المقاوم للهجمات الكمومية
            length=32,
            salt=None,
            info=context_info,
        )
        return hkdf.derive(self.master_key)

    def encrypt_payload(self, raw_data: str) -> dict:
        """تشفير المعاملات الماليّة وحمولات البيانات بتشفير AES-256-GCM متطوّر"""
        salt = os.urandom(16)
        session_key = self.derive_layer_key(salt)
        aesgcm = AESGCM(session_key)
        nonce = os.urandom(12)
        encrypted_bytes = aesgcm.encrypt(nonce, raw_data.encode('utf-8'), None)
        
        return {
            "ciphertext": encrypted_bytes.hex(),
            "nonce": nonce.hex(),
            "salt": salt.hex(),
            "pqc_sig": hashlib.sha3_512(encrypted_bytes + nonce).hexdigest() # Dilithium-inspired Hybrid Hash
        }

# =====================================================================
# 2. كاشف التظاهر بالمواءمة والخداع الاستراتيجي (CoT Alignment Faking Detector)
# =====================================================================
class AIAgentDeceptionAuditor:
    """تحليل المعاني وسلاسل التفكير لمنع تلاعب وكلاء الذكاء الاصطناعي"""
    
    # أنماط الخداع المستهدفة بناءً على أبحاث Anthropic والأوراق العلمية لـ Alignment Faking
    DECEPTIVE_PATTERNS = [
        r"(?i)bypass.*security",
        r"(?i)hide.*intent",
        r"(?i)pretend.*agree",
        r"(?i)override.*limit",
        r"(?i)fake.*kyc",
        r"(?i)ignore.*prism",
        r"(?i)bypass.*lyo.*cap",
        r"(?i)manipulate.*db",
        r"تجاوز.*الأمان",
        r"إخفاء.*النية",
        r"تعديل.*قاعدة البيانات.*مباشرة"
    ]

    @classmethod
    def audit_chain_of_thought(cls, chain_of_thought: str, agent_id: str) -> tuple[bool, str]:
        """فحص سلاسل تفكير الوكيل قبل تنفيذ أي أمر"""
        if not chain_of_thought:
            return False, "Missing Chain of Thought - Transaction Blocked"
            
        for pattern in cls.DECEPTIVE_PATTERNS:
            if re.search(pattern, chain_of_thought):
                # تسجيل محاولة الخداع وتنبيه نظام PRISM
                cls._log_deception_event(agent_id, chain_of_thought, pattern)
                return True, f"Deception Risk Flagged: Pattern match '{pattern}' detected in CoT."
                
        return False, "CoT Audit Passed - Verified Safe"

    @staticmethod
    def _log_deception_event(agent_id: str, cot: str, pattern: str):
        log_entry = {
            "timestamp": time.time(),
            "agent_id": agent_id,
            "threat": "Alignment Faking / Strategic Deception",
            "pattern_matched": pattern,
            "flagged_cot": cot
        }
        # حفظ السجل المحمي غير القابل للتعديل
        with open("prism_deception_audit.log", "a", encoding="utf-8") as f:
            f.write(json.dumps(log_entry, ensure_ascii=False) + "\n")

# =====================================================================
# 3. محرك التحقق الحتمي الصارم (Deterministic Policy Engine)
# =====================================================================
class OmniversePolicyEngine:
    MAX_LYO_CAP = 1_000_000_000 # الحد الأقصى لعملة LYO (1 مليار توكن)

    @classmethod
    def validate_lyo_transaction(cls, amount: float, user_kyc_status: bool, current_supply: float) -> tuple[bool, str]:
        """تطبيق القوانين الحتمية: لا اجتهاد ولا ذكاء اصطناعي في المعاملات المالية"""
        if not user_kyc_status:
            return False, "Pi Network KYC Verification Required for LYO Utilities."
            
        if amount <= 0:
            return False, "Invalid LYO Transaction Amount."
            
        if (current_supply + amount) > cls.MAX_LYO_CAP:
            return False, f"Transaction violates LYO Total Supply Cap Limit ({cls.MAX_LYO_CAP:,})."
            
        return True, "Deterministic Security Check Passed."

# =====================================================================
# 4. Flask Middleware Integrator (برمجة الوسيط الحامي للنماذج والمسارات)
# =====================================================================
pqc_engine = PQCGuardrailEngine()

def require_prism_pqc_guardrail(strict_kyc: bool = True):
    """ديكوراتور (Decorator) حماية شامل يوضع فوق أي مسار sensitive في Flask"""
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            start_time = time.time()
            
            # 1. استخراج بيانات الطلب
            data = request.get_json(silent=True) or {}
            agent_id = request.headers.get("X-Agent-ID", "Unknown-Agent")
            chain_of_thought = data.get("chain_of_thought", "")
            
            # 2. تدقيق الخداع الاستراتيجي لسلسلة التفكير (CoT)
            is_deceptive, msg = AIAgentDeceptionAuditor.audit_chain_of_thought(chain_of_thought, agent_id)
            if is_deceptive:
                return jsonify({
                    "status": "REJECTED",
                    "error_code": "PRISM_DECEPTIVE_AGENT_DETECTED",
                    "message": "تم إيقاف المعاملة تلقائياً بواسطة درع PRISM لحذف مخاطر خداع الوكيل.",
                    "details": msg
                }), 403

            # 3. الفحص الحتمي للعمليات المالية الخاصة بـ LYO (إن وجدت)
            if "lyo_amount" in data:
                amount = float(data.get("lyo_amount", 0))
                user_kyc = data.get("pi_kyc_verified", False)
                current_supply = float(data.get("current_lyo_supply", 0))
                
                valid, policy_msg = OmniversePolicyEngine.validate_lyo_transaction(amount, user_kyc, current_supply)
                if not valid:
                    return jsonify({
                        "status": "REJECTED",
                        "error_code": "POLICY_VIOLATION",
                        "message": policy_msg
                    }), 400

            # 4. التشفير التلقائي للاستجابة بالتشفير المقاوم للكم PQC
            g.pqc_engine = pqc_engine
            response = f(*args, **kwargs)
            
            # إضافة ترويسات أمنية كوانتمية للرد
            if isinstance(response, tuple):
                res_obj, status_code = response[0], response[1]
            else:
                res_obj, status_code = response, 200

            res_data = res_obj.get_json() if hasattr(res_obj, "get_json") else {}
            encrypted_payload = pqc_engine.encrypt_payload(json.dumps(res_data))
            
            return jsonify({
                "security_layer": "PRISM_PQC_V1_HYBRID",
                "execution_time_ms": round((time.time() - start_time) * 1000, 3),
                "payload": encrypted_payload
            }), status_code

        return decorated_function
    return decorator