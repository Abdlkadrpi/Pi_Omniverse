import os
import sqlite3
from flask import Blueprint, jsonify, request
from .crypto_pqc import PostQuantumSecurity
from .prism_audit import PRISMAISupervisor

lyo_voting_bp = Blueprint("lyo_voting", __name__)
PQC_SECRET_KEY = b"Omniverse_Tripoli_Node_PQC_Secret_2026"

# مسار قاعدة البيانات المحلية لتوثيق الأصوات (Digital Notary)
DB_PATH = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "../../assets.db")
)


def init_voting_db():
  with sqlite3.connect(DB_PATH) as conn:
    cursor = conn.cursor()
    cursor.execute("""
            CREATE TABLE IF NOT EXISTS lyo_votes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                pi_uid TEXT NOT NULL,
                proposal_id TEXT NOT NULL,
                choice BOOLEAN NOT NULL,
                weight REAL NOT NULL,
                pqc_signature TEXT NOT NULL,
                audit_status TEXT NOT NULL,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        """)
    conn.commit()


# تهيئة جدول التصويت عند بدء التشغيل تلقائياً
init_voting_db()


@lyo_voting_bp.route("/api/v1/lyo/vote", methods=["POST"])
def cast_secure_vote():
  data = request.get_json() or {}

  pi_uid = data.get("pi_uid")
  proposal_id = data.get("proposal_id")
  vote_choice = data.get("vote_choice", True)
  user_kyc_verified = data.get("kyc_verified", False)
  lyo_balance = float(data.get("lyo_balance", 0.0))

  # 1. التحقق الإلزامي من سياسة شبكة باي (Pi Network KYC Policy)
  if not user_kyc_verified:
    return (
        jsonify({
            "error": "KYC_REQUIRED",
            "message": (
                "يتطلب التصويت وحوكمة عملة LYO اجتياز مرحلة KYC الخاصة بشبكة باي"
                " حصرياً."
            ),
        }),
        403,
    )

  if lyo_balance <= 0:
    return (
        jsonify({
            "error": "INSUFFICIENT_LYO",
            "message": (
                "رصيد عملة المنفعة LYO غير كافٍ للمشاركة في وزن التصويت."
            ),
        }),
        400,
    )

  # 2. إعداد حمولة البيانات والتوقيع المقاوم للكم (PQC)
  payload_string = f"{pi_uid}:{proposal_id}:{vote_choice}:{lyo_balance}"
  pqc_sig = PostQuantumSecurity.generate_pqc_signature(
      payload_string, PQC_SECRET_KEY
  )

  # 3. تدقيق مشرف الذكاء الاصطناعي PRISM
  audit_result = PRISMAISupervisor.audit_vote(pi_uid, proposal_id, lyo_balance)

  if audit_result["status"] != "APPROVED_BY_PRISM":
    return (
        jsonify({
            "error": "PRISM_REJECTED",
            "message": "تم رفض التصويت بناءً على تقييم المخاطر الأمنية.",
        }),
        400,
    )

  # 4. التوثيق الرقمي الفوري في قاعدة البيانات SQLite (Digital Notary Ledger)
  try:
    with sqlite3.connect(DB_PATH) as conn:
      cursor = conn.cursor()
      cursor.execute(
          """
                INSERT INTO lyo_votes (pi_uid, proposal_id, choice, weight, pqc_signature, audit_status)
                VALUES (?, ?, ?, ?, ?, ?)
            """,
          (
              pi_uid,
              proposal_id,
              vote_choice,
              lyo_balance,
              pqc_sig,
              audit_result["status"],
          ),
      )
      conn.commit()
  except Exception as e:
    return (
        jsonify({
            "error": "DATABASE_ERROR",
            "message": f"فشل تسجيل الصوت في دفتر التوثيق الرقمي: {str(e)}",
        }),
        500,
    )

  return (
      jsonify({
          "status": "SUCCESS",
          "message": (
              "تم تسجيل وتأكيد وتوثيق التصويت رقمياً بنجاح تحت درع حماية PQC"
              " ومشرف PRISM."
          ),
          "pqc_signature": pqc_sig,
          "audit": audit_result,
      }),
      200,
  )