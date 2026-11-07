from flask import Blueprint, request, jsonify, session
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
