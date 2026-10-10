import os
import datetime
import time

# مسار خزنة الموثق التي يراقبها الوكيل
VAULT_PATH = r"C:\Users\الريادة للحاسبات\Desktop\Omniverse\Omniverse_Notary_Vault"

def run_test():
    print("🧪 جاري بدء اختبار التوثيق التلقائي...")
    
    # التأكد من وجود المجلد
    if not os.path.exists(VAULT_PATH):
        os.makedirs(VAULT_PATH)
    
    # إنشاء اسم ملف فريد بناءً على الوقت
    timestamp = datetime.datetime.now().strftime("%H_%M_%S")
    file_name = f"Test_Document_{timestamp}.txt"
    file_path = os.path.join(VAULT_PATH, file_name)
    
    # محتوى الملف التجريبي
    content = f"""
    Omniverse Digital Notary - Auto Test
    Status: Testing Production Environment
    Location: Tripoli - Arriyada Computers
    Timestamp: {datetime.datetime.now()}
    Verified by: AI Autonomous Agent
    """
    
    try:
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(content)
        print(f"✅ تم إنشاء ملف الاختبار: {file_name}")
        print(f"🚀 انتظر الآن رسالة التليجرام خلال ثوانٍ...")
    except Exception as e:
        print(f"❌ فشل الاختبار: {e}")

if __name__ == "__main__":
    run_test()