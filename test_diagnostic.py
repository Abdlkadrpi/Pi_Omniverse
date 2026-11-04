import os
import sqlite3
from datetime import datetime
from archive_transactions import init_ledger_database, archive_verified_transaction

# تحديد مسار قاعدة البيانات
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
DB_PATH = os.path.join(BASE_DIR, "assets.db")

def run_diagnostic():
    print("=" * 70)
    print("[*] بدء الفحص التشخيصي المباشر لأرشيف عقدة طرابلس...")
    print(f"[*] مسار قاعدة البيانات المستهدف: {DB_PATH}")
    print("=" * 70)

    # 1. تهيئة قاعدة البيانات والجدول
    init_ledger_database()

    # 2. إنشاء نموذج رد تجريبي متطابق مع استجابة الخادم
    sample_response = {
        "status": "success",
        "message": "Diagnostic test validation passed.",
        "cyber_security": {
            "pqc_signature_verified": True,
            "prism_guardrail_status": "PASSED",
            "timestamp": datetime.utcnow().timestamp()
        },
        "transaction_details": {
            "pi_user_uid": "tripoli_node_diagnostic_admin",
            "service_type": "diagnostic_test_task",
            "gross_paid_lyo": 100.0,
            "net_allocated_lyo": 99.0,
            "burned_lyo": 1.0,
            "burn_address": "0x000000000000000000000000000000000000DEAD",
            "node_origin": "Tripoli_Node_Gate_01"
        }
    }

    print("[*] جاري استدعاء دالة الأرشفة مباشرة...")
    success = archive_verified_transaction(sample_response)
    
    if success:
        print("[✔] نجحت عملية الأرشفة المباشرة!")
    else:
        print("[-] فشلت عملية الأرشفة المباشرة.")
        return

    # 3. قراءة البيانات مباشرة من الجدول للتأكد من وجودها
    print("\n[*] جاري فحص محتويات جدول sovereign_ledger_archive محلياً...")
    try:
        with sqlite3.connect(DB_PATH) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM sovereign_ledger_archive ORDER BY id DESC LIMIT 3;")
            rows = cursor.fetchall()

            print(f"[+] إجمالي الصفوف المسترجعة بالفحص: {len(rows)}")
            for idx, row in enumerate(rows, 1):
                print(f"  • صف [{idx}] -> ID: {row['id']} | TX_ID: {row['transaction_id']} | User: {row['pi_user_uid']} | Gross: {row['gross_paid_lyo']} LYO")
    except Exception as e:
        print(f"[-] خطأ أثناء قراءة الجدول: {e}")

    print("=" * 70)
    print("[*] انتهى الفحص التشخيصي بنجاح.")

if __name__ == "__main__":
    run_diagnostic()