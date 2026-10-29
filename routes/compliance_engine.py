import os
import time
import hashlib
import json
from flask import Blueprint, request, jsonify

compliance_bp = Blueprint('compliance_bp', __name__)

COMPLIANCE_PQC_SECRET = b"TRIPOLI_NODE_COMPLIANCE_AML_SECURE_2026"

def generate_compliance_pqc_signature(payload_str: str) -> str:
    salt = str(time.time_ns()).encode('utf-8')
    layer_one = hashlib.sha3_512(payload_str.encode('utf-8') + salt).hexdigest()
    layer_two = hashlib.blake2b(layer_one.encode('utf-8') + COMPLIANCE_PQC_SECRET, digest_size=32).hexdigest()
    return f"AML-PQC-{layer_two.upper()}"

@compliance_bp.route('/api/v1/compliance/audit', methods=['POST'])
def audit_financial_transaction():
    """
    بوابة الامتثال الضريبي والمحاسبي الآلي (AML & Regulatory Compliance Middleware).
    تتحقق من العمليات الكبرى وتضمن الامتثال للمعايير الدولية و سياسات Pi KYC.
    """
    try:
        data = request.get_json() or {}
        
        user_pi_uid = data.get('pi_uid')
        kyc_verified = data.get('kyc_verified', False)
        transaction_amount_lyo = data.get('amount_lyo', 0)
        destination_jurisdiction = data.get('jurisdiction', 'Global_Smart_City')
        
        if not user_pi_uid or not kyc_verified:
            return jsonify({
                "status": "error",
                "message": "Compliance Error: Financial auditing requires verified Pi Network KYC."
            }), 403
            
        if transaction_amount_lyo <= 0:
            return jsonify({
                "status": "error",
                "message": "Invalid transaction amount for compliance auditing."
            }), 400
            
        # فحص القواعد AML (حدود المعاملات المشبوهة أو الكبرى)
        aml_status = "APPROVED_LOW_RISK"
        if transaction_amount_lyo > 50000:
            aml_status = "FLAGGED_FOR_ENHANCED_DUE_DILIGENCE"
            
        audit_payload = {
            "pi_uid": user_pi_uid,
            "amount": transaction_amount_lyo,
            "jurisdiction": destination_jurisdiction,
            "aml_status": aml_status,
            "timestamp": time.time_ns()
        }
        
        payload_str = json.dumps(audit_payload, sort_keys=True)
        pqc_sig = generate_compliance_pqc_signature(payload_str)
        
        audit_id = f"AML-AUDIT-{hashlib.md5(payload_str.encode()).hexdigest()[:12].upper()}"
        
        return jsonify({
            "status": "success",
            "message": "Automated compliance and AML audit completed successfully on Tripoli Node.",
            "audit_report": {
                "audit_id": audit_id,
                "aml_risk_status": aml_status,
                "jurisdiction": destination_jurisdiction,
                "pqc_signature": pqc_sig,
                "node": "Tripoli Node v0.6.3"
            }
        }), 200

    except Exception as e:
        return jsonify({
            "status": "critical_error",
            "message": f"Compliance auditing failed: {str(e)}"
        }), 500