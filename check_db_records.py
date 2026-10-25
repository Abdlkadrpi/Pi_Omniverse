import sqlite3
import os
import json

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "assets.db")

def verify_database_records():
    if not os.path.exists(DB_PATH):
        print(f"[-] خطأ: قاعدة البيانات غير موجودة في المسار: {DB_PATH}")
        return

    print("[*] جاري الاتصال بقاعدة البيانات المحلية (assets.db)...")
    
    try:
        with sqlite3.connect(DB_PATH) as conn:
            cursor = conn.cursor()
            
            # 1. استعلام جدول الأصول (assets) للتحقق من تسجيل معاملة LYO الأخيرة
            print("\n--- آخر المعاملات المسجلة في جدول الأصول (assets) ---")
            cursor.execute("SELECT id, asset_name, asset_value, owner_id, payment_tx, timestamp FROM assets ORDER BY id DESC LIMIT 5")
            assets = cursor.fetchall()
            
            if not assets:
                print("[!] جدول الأصول فارغ حالياً.")
            else:
                for row in assets:
                    print(f"ID: {row[0]} | Name: {row[1]} | Value: {row[2]} LYO | Owner: {row[3]} | Tx: {row[4]} | Time: {row[5]}")

            # 2. استعلام جدول سجلات التدقيق (audit_logs) للتحقق من نشاط حراسة PRISM
            print("\n--- آخر سجلات المراقبة والتدقيق (audit_logs) ---")
            cursor.execute("SELECT id, agent_action, details, timestamp FROM audit_logs ORDER BY id DESC LIMIT 5")
            logs = cursor.fetchall()
            
            if not logs:
                print("[!] سجلات التدقيق فارغة حالياً.")
            else:
                for row in logs:
                    print(f"Log ID: {row[0]} | Action: {row[1]} | Details: {row[2]} | Time: {row[3]}")
                    
    except Exception as e:
        print(f"[-] حدث خطأ أثناء قراءة قاعدة البيانات: {str(e)}")

if __name__ == "__main__":
    verify_database_records()