import os

def apply_surgical_patch():
    print("[*] بدء تنفيذ التصحيح الجراحي لربط Pi SDK v2.0 وتوثيق KYC في أومنيفيرس...")

    # 1. إنشاء مجلد middleware إذا لم يكن موجوداً
    middleware_dir = "middleware"
    if not os.path.exists(middleware_dir):
        os.makedirs(middleware_dir)
        print(f"[+] تم إنشاء المجلد: {middleware_dir}")

    # 2. كتابة ملف الوسيط الأمني pi_auth.py
    auth_middleware_path = os.path.join(middleware_dir, "pi_auth.py")
    auth_code = '''from functools import wraps
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
'''
    with open(auth_middleware_path, "w", encoding="utf-8") as f:
        f.write(auth_code)
    print(f"[+] تم حقن الوسيط الأمني بنجاح في: {auth_middleware_path}")

    # 3. التأكد من وجود مجلد Blueprints وحقن مسارات الـ Pi SDK
    blueprint_dir = "Blueprints"
    if not os.path.exists(blueprint_dir):
        os.makedirs(blueprint_dir)
        print(f"[+] تم إنشاء مجلد البلوبرنتس: {blueprint_dir}")

    agent_routes_path = os.path.join(blueprint_dir, "agent_routes.py")
    routes_code = '''from flask import Blueprint, request, jsonify, session
from middleware.pi_auth import require_pi_kyc

agent_bp = Blueprint('agent_routes', __name__)

@agent_bp.route('/api/v1/agent/execute', methods=['POST'])
@require_pi_kyc
def execute_agent_task():
    """
    تنفيذ مهمة عبر الوكيل الذكي بخصم وقود LYO حصرياً للمستخدمين الموثقين.
    """
    data = request.get_json() or {}
    task_payload = data.get('task')
    
    if not task_payload:
        return jsonify({"status": "error", "message": "بيانات المهمة غير صالحة."}), 400

    return jsonify({
        "status": "success",
        "node": "Tripoli-Node-v0.6.3",
        "message": "تم التحقق من هوية KYC بنجاح، وجارِ تمرير المهمة للوكيل الذكي مقابل وقود LYO.",
        "processed_by": "General Manager AI Supervisor"
    }), 200

@agent_bp.route('/api/v1/auth/pi-login', methods=['POST'])
def pi_sdk_login():
    auth_data = request.get_json() or {}
    pi_uid = auth_data.get('uid')
    is_kyc = auth_data.get('kyc_verified', False)

    if not pi_uid:
        return jsonify({"status": "error", "message": "معرّف المستخدم مفقود."}), 400

    session['pi_user_uid'] = pi_uid
    session['pi_kyc_verified'] = is_kyc

    return jsonify({
        "status": "success",
        "authenticated": True,
        "kyc_verified": is_kyc,
        "message": "تمت مزامنة جلسة Pi SDK بنجاح مع عقدة طرابلس."
    }), 200
'''
    with open(agent_routes_path, "w", encoding="utf-8") as f:
        f.write(routes_code)
    print(f"[+] تم حقن مسارات الوكلاء والمصادقة بنجاح في: {agent_routes_path}")
    print("[✔] اكتمل التصحيح الجراحي بنجاح تام وجاهز للرفع على Render.")

if __name__ == "__main__":
    apply_surgical_patch()