import functools
import logging
import re
from flask import jsonify, request

# ضبط سجلات الأمان لعقدة طرابلس
logger = logging.getLogger("TripoliNodeSecurity")
logger.setLevel(logging.INFO)


class TripoliNodeGuardrail:
    """درع الأمان الخاص بسيرفر عقدة طرابلس (Port 5000)

    لحماية وكلاء PRISM والتحكم بالصلاحيات المالية لـ LYO و Pi Network.
    """

    # أنماط الهجمات السيبرانية وحقن الأوامر (Prompt Injection)
    RESTRICTED_PATTERNS = [
        r"ignore\s+previous\s+instructions",
        r"override\s+system",
        r"drop\s+database",
        r"delete\s+from",
        r"exec\s*\(",
        r"eval\s*\(",
        r"sudo\s+",
        r"grant\s+all",
    ]

    @classmethod
    def is_safe_prompt(cls, prompt: str) -> bool:
        """فحص المدخلات البرمجية الموجهة للوكلاء الذكيين"""
        if not prompt or not isinstance(prompt, str):
            return True

        lowered = prompt.lower()
        for pattern in cls.RESTRICTED_PATTERNS:
            if re.search(pattern, lowered):
                logger.warning(
                    f"[TRIPOLI_NODE_SECURITY] تم اكتشاف نمط مشبوه: {pattern}"
                )
                return False
        return True

    @classmethod
    def verify_lyo_transfer(cls, amount: float, role: str) -> tuple[bool, str]:
        """التحقق من حواجز تحويلات LYO (سقف الصلاحية للتحويل الآلي 1000 LYO)"""
        LIMIT = 1000.0
        if amount > LIMIT and role != "GENERAL_MANAGER":
            return (
                False,
                "تنبيه: تحويل هذا المبلغ يطلب موافقة يدوية مشفرة من المدير العام (General Manager HITL).",
            )
        return True, "العملية ضمن الحدود المسموح بها."


def enforce_node_security(f):
    """Decorator لحماية مسارات وكلاء عقدة طرابلس مع استثناء طلبات القراءة GET"""

    @functools.wraps(f)
    def decorated_function(*args, **kwargs):
        # السماح الفوري لطلبات القراءة (GET) بالمرور دون قيود صارمة
        if request.method == "GET":
            return f(*args, **kwargs)

        # لفحص طلبات الكتابة والإرسال (POST / PUT وغيرها)
        data = request.get_json(silent=True) or {}
        prompt = data.get("prompt", "")
        amount = float(data.get("amount", 0.0))
        role = data.get("role", "USER")

        # 1. فحص حقن الأوامر في وكلاء PRISM
        if not TripoliNodeGuardrail.is_safe_prompt(prompt):
            return (
                jsonify(
                    {
                        "status": "blocked",
                        "error": "SECURITY_VIOLATION",
                        "message": "تم حظر الطلب من عقدة طرابلس: رصد محاولة تجاوز الصلاحيات أو حقن أوامر.",
                    }
                ),
                403,
            )

        # 2. فحص الحدود المالية لـ LYO
        is_valid_amount, msg = TripoliNodeGuardrail.verify_lyo_transfer(
            amount, role
        )
        if not is_valid_amount:
            return (
                jsonify(
                    {
                        "status": "pending_approval",
                        "error": "HITL_REQUIRED",
                        "message": msg,
                    }
                ),
                402,
            )

        return f(*args, **kwargs)

    return decorated_function