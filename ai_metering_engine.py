from datetime import datetime
import sqlite3
from flask import Blueprint, jsonify, request

ai_metering_bp = Blueprint("ai_metering_bp", __name__)

DB_PATH = "assets.db"  # قاعدة البيانات المحلية في عقدة طرابلس


def init_db():
  """إنشاء جدول الأرصدة وسجلات الحوسبة إذا لم يكن موجوداً"""
  conn = sqlite3.connect(DB_PATH)
  cursor = conn.cursor()
  cursor.execute("""
        CREATE TABLE IF NOT EXISTS lyo_ledger (
            user_id TEXT PRIMARY KEY,
            balance REAL NOT NULL
        )
    """)
  cursor.execute("""
        CREATE TABLE IF NOT EXISTS ai_audit_logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id TEXT,
            tokens INTEGER,
            cost REAL,
            status TEXT,
            timestamp TEXT
        )
    """)
  # إدراج مستخدم افتراضي للتجربة إذا لم يكن موجوداً
  cursor.execute(
      "INSERT OR IGNORE INTO lyo_ledger (user_id, balance) VALUES (?, ?)",
      ("user_abd_01", 1000.0),
  )
  conn.commit()
  conn.close()


# تشغيل تهيئة القاعدة عند التحميل
init_db()

# معدل التسعير لكل 1000 رمز
LYO_PER_1K_TOKENS = 0.005


@ai_metering_bp.route("/api/ai/metered-consume", methods=["POST"])
def metered_consume():
  data = request.get_json()
  user_id = data.get("user_id", "user_abd_01")
  prompt_tokens = data.get("prompt_tokens", 0)
  completion_tokens = data.get("completion_tokens", 0)
  total_tokens = prompt_tokens + completion_tokens

  # 🛡️ محاكاة الحماية من الهجمات السيبرانية (Cyber Attack & Anomaly Simulation)
  # 1. فحص الهجمات الحجمية أو طلبات حرمان الخدمة (DoS / Prompt Bombing)
  if total_tokens > 50000:
    log_audit(user_id, total_tokens, 0, "BLOCKED_DOS_ATTEMPT")
    return jsonify({
        "status": "security_block",
        "reason": (
            "PRISM Supervisor detected abnormal token inflation (Potential"
            " DoS Attack)."
        ),
    }), 403

  # 2. فحص التلاعب أو الحقن السريع (Spam / Replay Injection Simulation)
  if prompt_tokens < 0 or completion_tokens < 0:
    log_audit(user_id, total_tokens, 0, "BLOCKED_MALFORMED_PACKET")
    return jsonify({
        "status": "security_block",
        "reason": "Invalid token parameters detected. Packet rejected.",
    }), 400

  # حساب التكلفة بعملة LYO
  cost_in_lyo = (total_tokens / 1000.0) * LYO_PER_1K_TOKENS

  conn = sqlite3.connect(DB_PATH)
  cursor = conn.cursor()

  # جلب رصيد المستخدم
  cursor.execute(
      "SELECT balance FROM lyo_ledger WHERE user_id = ?", (user_id,)
  )
  row = cursor.fetchone()

  if not row:
    conn.close()
    return jsonify({"error": "User not found in LYO ledger"}), 404

  current_balance = row[0]

  # التحقق من كفاية الرصيد
  if current_balance < cost_in_lyo:
    conn.close()
    log_audit(user_id, total_tokens, cost_in_lyo, "REJECTED_INSUFFICIENT_FUNDS")
    return jsonify({
        "status": "payment_required",
        "reason": "Insufficient LYO balance for compute execution.",
        "required_lyo": cost_in_lyo,
        "current_balance": current_balance,
    }), 402

  # خصم الرصيد وتحديث قاعدة البيانات محلياً
  new_balance = current_balance - cost_in_lyo
  cursor.execute(
      "UPDATE lyo_ledger SET balance = ? WHERE user_id = ?",
      (new_balance, user_id),
  )
  conn.commit()
  conn.close()

  # تسجيل العملية بنجاح عبر PRISM
  log_audit(user_id, total_tokens, cost_in_lyo, "SUCCESS")

  return jsonify({
      "status": "success",
      "meter_metrics": {
          "tokens_consumed": total_tokens,
          "cost_deducted_lyo": cost_in_lyo,
          "remaining_lyo_balance": new_balance,
      },
      "prism_supervisor": "Verified & Secured",
      "timestamp": datetime.utcnow().isoformat(),
  })


def log_audit(user_id, tokens, cost, status):
  """تسجيل تدقيق أمني لتصرفات الوكلاء والاستهلاك"""
  conn = sqlite3.connect(DB_PATH)
  cursor = conn.cursor()
  cursor.execute(
      """
        INSERT INTO ai_audit_logs (user_id, tokens, cost, status, timestamp)
        VALUES (?, ?, ?, ?, ?)
    """,
      (user_id, tokens, cost, status, datetime.utcnow().isoformat()),
  )
  conn.commit()
  conn.close()