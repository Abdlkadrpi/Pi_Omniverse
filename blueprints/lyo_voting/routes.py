from flask import Blueprint, request, jsonify
from .crypto_pqc import PostQuantumSecurity
from .prism_audit import PRISMAISupervisor

lyo_voting_bp = Blueprint('lyo_voting', __name__)
PQC_SECRET_KEY = b"Omniverse_Tripoli_Node_PQC_Secret_2026"
VOTES_DB = {}

@lyo_voting_bp.route('/api/v1/lyo/vote', methods=['POST'])
def cast_secure_vote():
    data = request.get_json() or {}
    
    pi_uid = data.get('pi_uid')
    proposal_id = data.get('proposal_id')
    vote_choice = data.get('vote_choice')
    user_kyc_verified = data.get('kyc_verified', False)
    lyo_balance = float(data.get('lyo_balance', 0.0))
    
    if not user_kyc_verified:
        return jsonify({
            "error": "KYC_REQUIRED",
            "message": "يتطلب التصويت اجتياز مرحلة KYC الخاصة بشبكة باي حصرياً."
        }), 403

    if lyo_balance <= 0:
        return jsonify({
            "error": "INSUFFICIENT_LYO",
            "message": "رصيد عملة المنفعة LYO غير كافٍ للمشاركة في وزن التصويت."
        }), 400

    payload_string = f"{pi_uid}:{proposal_id}:{vote_choice}:{lyo_balance}"
    pqc_sig = PostQuantumSecurity.generate_pqc_signature(payload_string, PQC_SECRET_KEY)
    audit_result = PRISMAISupervisor.audit_vote(pi_uid, proposal_id, lyo_balance)

    if audit_result["status"] != "APPROVED_BY_PRISM":
        return jsonify({
            "error": "PRISM_REJECTED",
            "message": "تم رفض التصويت بناءً على تقييم المخاطر الأمنية."
        }), 400

    vote_record = {
        "pi_uid": pi_uid,
        "proposal_id": proposal_id,
        "choice": vote_choice,
        "weight": lyo_balance,
        "pqc_signature": pqc_sig,
        "audit_meta": audit_result
    }
    
    if proposal_id not in VOTES_DB:
        VOTES_DB[proposal_id] = []
    
    VOTES_DB[proposal_id].append(vote_record)

    return jsonify({
        "status": "SUCCESS",
        "message": "تم تسجيل وتأكيد التصويت بنجاح تحت درع حماية PQC ومشرف PRISM.",
        "pqc_signature": pqc_sig,
        "audit": audit_result
    }), 200
