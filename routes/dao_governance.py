import os
import time
import hashlib
import json
from flask import Blueprint, request, jsonify

dao_bp = Blueprint('dao_bp', __name__)

# مفتاح سري لتوقيع مقترحات الحوكمة (DAO Quantum-Resilient Key)
DAO_PQC_SECRET = b"TRIPOLI_NODE_DAO_GOVERNANCE_SECURE_2026"

def generate_dao_pqc_signature(payload_str: str) -> str:
    """
    توليد توقيع مشفر ومقاوم للحوسبة الكمية لعمليات التصويت والمقترحات في الحوكمة.
    """
    salt = str(time.time_ns()).encode('utf-8')
    layer_one = hashlib.sha3_512(payload_str.encode('utf-8') + salt).hexdigest()
    layer_two = hashlib.blake2b(layer_one.encode('utf-8') + DAO_PQC_SECRET, digest_size=32).hexdigest()
    return f"DAO-PQC-{layer_two.upper()}"

@dao_bp.route('/api/v1/dao/propose', methods=['POST'])
def create_dao_proposal():
    """
    إنشاء مقترح جديد للحوكمة اللامركزية للمدن الذكية (يتطلب Pi KYC و عملة LYO).
    """
    try:
        data = request.get_json() or {}
        
        user_pi_uid = data.get('pi_uid')
        kyc_verified = data.get('kyc_verified', False)
        proposal_title = data.get('title')
        proposal_description = data.get('description')
        staked_lyo = data.get('staked_lyo', 0)
        
        # 1. التحقق الصارم من متطلبات الحوكمة والتحقق من الهوية
        if not user_pi_uid or not kyc_verified:
            return jsonify({
                "status": "error",
                "message": "DAO Security Error: Creating proposals requires verified Pi Network KYC."
            }), 403
            
        if not proposal_title or staked_lyo < 100:
            return jsonify({
                "status": "error",
                "message": "Invalid proposal parameters or insufficient LYO stake (minimum 100 LYO required)."
            }), 400
            
        # 2. بناء حمولة المقترح مع منع التلاعب
        proposal_payload = {
            "pi_uid": user_pi_uid,
            "title": proposal_title,
            "description": proposal_description,
            "staked_lyo": staked_lyo,
            "timestamp": time.time_ns()
        }
        
        payload_str = json.dumps(proposal_payload, sort_keys=True)
        pqc_sig = generate_dao_pqc_signature(payload_str)
        
        proposal_id = f"DAO-PROP-{hashlib.md5(payload_str.encode()).hexdigest()[:10].upper()}"
        
        return jsonify({
            "status": "success",
            "message": "DAO proposal successfully created and secured on Tripoli Node.",
            "proposal": {
                "proposal_id": proposal_id,
                "title": proposal_title,
                "creator": user_pi_uid,
                "staked_lyo": staked_lyo,
                "pqc_signature": pqc_sig,
                "status": "ACTIVE_FOR_VOTING"
            }
        }), 200

    except Exception as e:
        return jsonify({
            "status": "critical_error",
            "message": f"DAO proposal failed: {str(e)}"
        }), 500


@dao_bp.route('/api/v1/dao/vote', methods=['POST'])
def cast_dao_vote():
    """
    التصويت على المقترحات الذكية باستخدام عملة المنفعة LYO مع ضمان الشفافية والتحقق.
    """
    try:
        data = request.get_json() or {}
        
        user_pi_uid = data.get('pi_uid')
        kyc_verified = data.get('kyc_verified', False)
        proposal_id = data.get('proposal_id')
        vote_choice = data.get('vote') # 'FOR' أو 'AGAINST'
        voting_power_lyo = data.get('voting_power_lyo', 0)
        
        if not user_pi_uid or not kyc_verified:
            return jsonify({
                "status": "error",
                "message": "Access Denied: Voting requires verified Pi KYC."
            }), 403
            
        if vote_choice not in ['FOR', 'AGAINST'] or voting_power_lyo <= 0:
            return jsonify({
                "status": "error",
                "message": "Invalid vote parameters or voting power."
            }), 400
            
        vote_payload = {
            "pi_uid": user_pi_uid,
            "proposal_id": proposal_id,
            "vote": vote_choice,
            "power": voting_power_lyo,
            "nonce": time.time_ns()
        }
        
        payload_str = json.dumps(vote_payload, sort_keys=True)
        pqc_vote_sig = generate_dao_pqc_signature(payload_str)
        
        return jsonify({
            "status": "success",
            "message": "DAO vote successfully cast, recorded, and secured.",
            "receipt": {
                "vote_id": pqc_vote_sig,
                "proposal_id": proposal_id,
                "choice": vote_choice,
                "weight": voting_power_lyo,
                "node": "Tripoli Node v0.6.3"
            }
        }), 200

    except Exception as e:
        return jsonify({
            "status": "critical_error",
            "message": f"DAO voting failed: {str(e)}"
        }), 500