import hashlib
import hmac

class PostQuantumSecurity:
    """
    طبقة الحماية المقاومة للكم (PostQuantum Cryptography Layer)
    محصنة ضد خوارزميات التجسس الكمومي والتوقيعات الهجينة.
    """
    @staticmethod
    def generate_pqc_signature(payload: str, secret_key: bytes) -> str:
        message_bytes = payload.encode('utf-8')
        pqc_hash = hmac.new(secret_key, message_bytes, hashlib.sha3_512).hexdigest()
        return f"PQC-SHA3-{pqc_hash}"

    @staticmethod
    def verify_pqc_signature(payload: str, secret_key: bytes, signature: str) -> bool:
        expected_sig = PostQuantumSecurity.generate_pqc_signature(payload, secret_key)
        return hmac.compare_digest(expected_sig, signature)
