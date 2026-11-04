import os
import sqlite3
import json
from datetime import datetime, timezone

# استخدام المسار المطلق الموحد لقاعدة البيانات في جذر المشروع
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
DB_PATH = os.path.join(BASE_DIR, "assets.db")

def init_ledger_database():
    """تهيئة جداول الأرشيف والتدقيق الخاصة بعقدة طرابلس إذا لم تكن موجودة"""
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        # جدول أرشفة المعاملات السيادية المؤكدة
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS sovereign_ledger_archive (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                transaction_id TEXT UNIQUE NOT NULL,
                pi_user_uid TEXT NOT NULL,
                service_type TEXT NOT NULL,
                gross_paid_lyo REAL NOT NULL,
                net_allocated_lyo REAL NOT NULL,
                burned_lyo REAL NOT NULL,
                burn_address TEXT NOT NULL,
                node_origin TEXT NOT NULL,
                pqc_verified BOOLEAN NOT NULL,
                timestamp TEXT NOT NULL,
                raw_response_json TEXT NOT NULL
            )
        """)
        conn.commit()

def archive_verified_transaction(response_data):
    """استلام رد المعاملات الناجحة (200 OK) وأرشفتها فوراً في السجل الدائم"""
    init_ledger_database()
    
    tx_details = response_data.get("transaction_details", {})
    cyber_security = response_data.get("cyber_security", {})
    
    # توليد معرف فريد للمعاملة بناءً على الطابع الزمني والمستخدم
    timestamp_raw = cyber_security.get("timestamp", datetime.now(timezone.utc).timestamp())
    tx_id = f"TRIPOLI-TX-{int(timestamp_raw * 1000)}"
    
    record = {
        "transaction_id": tx_id,
        "pi_user_uid": tx_details.get("pi_user_uid", "unknown_user"),
        "service_type": tx_details.get("service_type", "default_task"),
        "gross_paid_lyo": tx_details.get("gross_paid_lyo", 0.0),
        "net_allocated_lyo": tx_details.get("net_allocated_lyo", 0.0),
        "burned_lyo": tx_details.get("burned_lyo", 0.0),
        "burn_address": tx_details.get("burn_address", "0x000000000000000000000000000000000000DEAD"),
        "node_origin": tx_details.get("node_origin", "Tripoli_Node_Gate_01"),
        "pqc_verified": cyber_security.get("pqc_signature_verified", True),
        "timestamp": datetime.fromtimestamp(timestamp_raw, tz=timezone.utc).strftime('%Y-%m-%d %H:%M:%S'),
        "raw_response_json": json.dumps(response_data, ensure_ascii=False)
    }

    try:
        with sqlite3.connect(DB_PATH) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT OR IGNORE INTO sovereign_ledger_archive (
                    transaction_id, pi_user_uid, service_type, gross_paid_lyo, 
                    net_allocated_lyo, burned_lyo, burn_address, node_origin, 
                    pqc_verified, timestamp, raw_response_json
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                record["transaction_id"],
                record["pi_user_uid"],
                record["service_type"],
                record["gross_paid_lyo"],
                record["net_allocated_lyo"],
                record["burned_lyo"],
                record["burn_address"],
                record["node_origin"],
                record["pqc_verified"],
                record["timestamp"],
                record["raw_response_json"]
            ))
            conn.commit()
            print(f"[✔] تم بنجاح أرشفة المعاملة برقم معرف: {tx_id} في دفتر أستاذ عقدة طرابلس.")
            return True
    except Exception as e:
        print(f"[-] خطأ أثناء أرشفة المعاملة في قاعدة البيانات: {e}")
        return False

if __name__ == "__main__":
    # محاكاة لبيانات رد ناجح من عقدة طرابلس لاختبار الأرشفة الفورية
    sample_successful_response = {
        "status": "success",
        "message": "Zero-Trust & Quantum-Resilient security validation passed.",
        "cyber_security": {
            "pqc_signature_verified": True,
            "prism_guardrail_status": "PASSED",
            "timestamp": datetime.now(timezone.utc).timestamp()
        },
        "transaction_details": {
            "pi_user_uid": "tripoli_node_admin_01",
            "service_type": "verify_node_ledger",
            "gross_paid_lyo": 50.0,
            "net_allocated_lyo": 49.5,
            "burned_lyo": 0.5,
            "burn_address": "0x000000000000000000000000000000000000DEAD",
            "node_origin": "Tripoli_Node_Gate_01"
        }
    }
    
    print("[*] جاري اختبار سكريبت الأرشفة الآلية لعقدة طرابلس...")
    archive_verified_transaction(sample_successful_response)