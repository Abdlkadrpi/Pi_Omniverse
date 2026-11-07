from functools import wraps
from flask import request, jsonify, session

def require_pi_kyc(f):
    """
    مُدقق أمني إجباري: يتحقق من أن المستخدم أكمل مرحلة KYC في شبكة باي
    ولديه جلسة مصادقة نشطة، تطابقاً مع سياسات النظام البيئي الجديدة.
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        pi_user_uid = session.get('pi_user_uid') or request.headers.get('X-Pi-User-Uid')
        kyc_status = session.get('pi_kyc_verified', False)

        if not pi_user_uid:
            return jsonify({
                "status": "error",
                "code": "AUTH_REQUIRED",
                "message": "غير مسجل. يجب المصادقة عبر Pi Network SDK للوصول إلى النظام البيئي لأومنيفيرس."
            }), 401

        if not kyc_status:
            return jsonify({
                "status": "error",
                "code": "KYC_REQUIRED",
                "message": "عذراً، يجب اجتياز مرحلة التحقق من الهوية (KYC) على شبكة باي لاستخدام وكلاء الذكاء الاصطناعي وعملة المنفعة LYO."
            }), 403

        return f(*args, **kwargs)
    return decorated_function
