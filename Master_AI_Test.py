import hashlib
import os
import requests
import datetime
import time

# --- إعدادات السيادة الرقمية (نود طرابلس - الريادة للحاسبات) ---
TOKEN = "8689618232:AAFIF8XzxpxnYfg37-vIJhKHYntUrvjB5sc"
CHAT_ID = "6043063504"
VAULT_PATH = r"C:\Users\الريادة للحاسبات\Desktop\Omniverse\Omniverse_Notary_Vault"
OLLAMA_URL = "http://localhost:11434/api/generate"

def ask_ollama(text):
    """استدعاء ذكاء TinyLlama المحلي مع زيادة وقت الانتظار لضمان التحليل"""
    print("🤖 جاري استشارة الذكاء الاصطناعي (TinyLlama)... يرجى الانتظار")
    
    prompt = f"Summarize this document in one short sentence in Arabic: {text}"
    
    try:
        # تم رفع الـ timeout إلى 120 ثانية لضمان استقرار المعالجة على جهازك
        response = requests.post(OLLAMA_URL, json={
            "model": "tinyllama:latest",
            "prompt": prompt,
            "stream": False
        }, timeout=120)
        
        if response.status_code == 200:
            return response.json().get("response", "تمت المعالجة بنجاح.")
        else:
            return f"⚠️ خطأ في الاستجابة (كود {response.status_code})"
    except requests.exceptions.Timeout:
        return "⏳ المعالج مستغرق في التفكير (Timeout).. جرب ملفاً أصغر أو أغلق البرامج المفتوحة."
    except Exception as e:
        return f"❌ فشل الاتصال بالمحرك: {str(e)}"

def send_telegram(msg):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    payload = {"chat_id": CHAT_ID, "text": msg, "parse_mode": "Markdown"}
    try:
        requests.post(url, json=payload)
        print("✅ تم إرسال التقرير النهائي بنجاح.")
    except:
        print("❌ فشل إرسال التقرير.")

def run_full_cycle():
    print("🚀 بدء دورة التوثيق والذكاء الاصطناعي الكاملة...")
    
    # 1. إنشاء وثيقة اختبار ذكية فريدة
    timestamp = datetime.datetime.now().strftime("%H_%M_%S")
    file_name = f"Final_Smart_Test_{timestamp}.txt"
    file_path = os.path.join(VAULT_PATH, file_name)
    
    content = f"""
    مستند توثيق رقمي فائق الأمان
    الجهة المصدرة: شركة الريادة للحاسبات
    المشروع: Omniverse Web3
    الهدف: تأمين البيانات عبر بصمة SHA-256 وتحليلها بذكاء محلي.
    التوقيت المحلي: {datetime.datetime.now()}
    """
    
    if not os.path.exists(VAULT_PATH):
        os.makedirs(VAULT_PATH)

    with open(file_path, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"✅ تم إنشاء الوثيقة: {file_name}")

    # 2. حساب البصمة الرقمية (Blockchain Standard)
    sha256 = hashlib.sha256()
    with open(file_path, "rb") as f:
        while chunk := f.read(4096): sha256.update(chunk)
    file_hash = sha256.hexdigest()
    print(f"🔐 تم توليد البصمة الرقمية: {file_hash[:10]}...")

    # 3. التحليل الذكي (AI Analysis)
    ai_analysis = ask_ollama(content)

    # 4. إرسال النتيجة النهائية
    final_msg = (
        f"🌟 *إنجاز تقني: التوثيق الذكي المكتمل*\n"
        f"━━━━━━━━━━━━━━━\n"
        f"📄 *الملف:* `{file_name}`\n"
        f"🔐 *بصمة الأمان:* `{file_hash}`\n\n"
        f"🤖 *تحليل AI (TinyLlama):*\n"
        f"_{ai_analysis.strip()}_\n\n"
        f"📍 *المصدر:* نود طرابلس - الريادة للحاسبات\n"
        f"⏰ *التوقيت:* {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
        f"━━━━━━━━━━━━━━━\n"
        f"✅ تمت الدورة الكاملة بنجاح."
    )
    
    send_telegram(final_msg)
    print("🏁 انتهت المهمة! تفقد هاتفك الآن.")

if __name__ == "__main__":
    run_full_cycle()