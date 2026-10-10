import os
import shutil
from datetime import datetime

# مسارات المشروع وملف قاعدة البيانات
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, 'assets.db')
BACKUP_DIR = os.path.join(BASE_DIR, 'cloud_backups')

def create_local_backup():
    if not os.path.exists(BACKUP_DIR):
        os.makedirs(BACKUP_DIR)
        
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    backup_filename = f"assets_backup_{timestamp}.db"
    backup_path = os.path.join(BACKUP_DIR, backup_filename)
    
    try:
        if os.path.exists(DB_PATH):
            shutil.copy2(DB_PATH, backup_path)
            print(f"[✔] تمت عملية النسخ الاحتياطي بنجاح محلياً: {backup_filename}")
        else:
            print("[!] تنبيه: قاعدة البيانات غير موجودة لتخزين نسخة احتياطية.")
    except Exception as e:
        print(f"[✘] فشل إنشاء النسخة الاحتياطية: {str(e)}")

if __name__ == "__main__":
    create_local_backup()