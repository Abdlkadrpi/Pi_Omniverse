from flask import Blueprint, request, jsonify
# استدعاء ملف الحوكمة من المجلد الرئيسي
from lyo_governance import LYOGovernanceEngine

lyo_blueprint = Blueprint('lyo_blueprint', __name__)
governance = LYOGovernanceEngine()

@lyo_blueprint.route('/api/v1/lyo/pay', methods=['POST'])
def pay_agent_service():
    """
    مسار معالجة مدفوعات الوكلاء الذكيين وعمليات الحرق التلقائي
    """
    data = request.get_json() or {}
    
    user_id = data.get('user_id')
    agent_id = data.get('agent_id')
    amount_lyo = float(data.get('amount_lyo', 0))
    is_kyc_verified = data.get('is_kyc_verified', False)

    try:
        # تنفيذ عملية الحوكمة والتحقق من الشروط الصارمة
        result = governance.process_agent_service_payment(
            user_id=user_id,
            agent_id=agent_id,
            amount_lyo=amount_lyo,
            is_kyc_verified=is_kyc_verified
        )
        return jsonify(result), 200
        
    except PermissionError as pe:
        return jsonify({"status": "SECURITY_BLOCK", "error": str(pe)}), 403
    except ValueError as ve:
        return jsonify({"status": "VALIDATION_ERROR", "error": str(ve)}), 400
    except Exception as e:
        return jsonify({"status": "ERROR", "error": str(e)}), 500