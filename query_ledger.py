import os
import sqlite3

# استخدام المسار المطلق الموحد لقاعدة البيانات في جذر المشروع لضمان التطابق التام
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
DB_PATH = os.path.join(BASE_DIR, "assets.db")

def query_archived_transactions():
    """استعلام وعرض كافة المعاملات المؤرشفة في دفتر أستاذ عقدة طرابلس"""
    print("=" * 70)
    print("[*] جاري الاتصال بدفتر أستاذ عقدة طرابلس (Tripoli Node Ledger)...")
    print(f"[*] مسار قاعدة البيانات المستخدم: {DB_PATH}")
    print("=" * 70)

    try:
        with sqlite3.connect(DB_PATH) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()

            # التأكد من وجود جدول الأرشيف أو إنشاؤه لضمان عدم وجود أخطاء
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

            # جلب كافة المعاملات مرتبة من الأحدث إلى الأقدم
            cursor.execute("SELECT * FROM sovereign_ledger_archive ORDER BY id DESC;")
            rows = cursor.fetchall()

            if not rows:
                print("[!] جدول الأرشيف جاهز، ولكن لا توجد معاملات مؤرشفة حتى الآن.")
                print("[*] نصيحة: تأكد من تشغيل خادم app.py وتنفيذ test_live_execution.py لتسجيل المعاملة تلقائياً.")
                return

            print(f"[+] تم العثور على ({len(rows)}) معاملة مؤرشفة بنجاح:\n")

            for idx, row in enumerate(rows, 1):
                print(f"--- معاملة رقم [{idx}] ---")
                print(f"  • معرف المعاملة (TX ID) : {row['transaction_id']}")
                print(f"  • المستخدم (Pi UID)    : {row['pi_user_uid']}")
                print(f"  • نوع الخدمة/المهمة    : {row['service_type']}")
                print(f"  • المبلغ الإجمالي     : {row['gross_paid_lyo']} LYO")
                print(f"  • الصافي المخصص       : {row['net_allocated_lyo']} LYO")
                print(f"  • نسبة الحرق (1%)     : {row['burned_lyo']} LYO")
                print(f"  • عنوان الحرق (Burn)   : {row['burn_address']}")
                print(f"  • مصدر العقدة          : {row['node_origin']}")
                print(f"  • التحقق الكمي (PQC)   : {'✅ مجتاز' if row['pqc_verified'] else '❌ مرفوض'}")
                print(f"  • الطابع الزمني        : {row['timestamp']}")
                print("-" * 70)

    except Exception as e:
        print(f"[-] حدث خطأ أثناء الاستعلام من قاعدة البيانات: {e}")

if __name__ == "__main__":
    query_archived_transactions()