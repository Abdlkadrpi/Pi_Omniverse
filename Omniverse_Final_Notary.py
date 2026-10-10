import hashlib
import os
import requests
import datetime
import time

# --- بيانات الهوية الرقمية (مؤكدة وسليمة) ---
TOKEN = "8689618232:AAFIF8XzxpxnYfg37-vIJhKHYntUrvjB5sc"
CHAT_ID = "6043063504"
VAULT_PATH = r"C:\Users\الريادة للحاسبات\Desktop\Omniverse\Omniverse_Notary_Vault"
OLLAMA_URL = "http://localhost:11434/api/generate"

def ask_ollama(text):
    """استدعاء ذكاء Ollama المحلي مع معالجة الأخطاء"""
    print("🤖 جاري استشارة الذكاء الاصطناعي Ollama...")
    prompt = f"لخص هذه الوثيقة في سطر واحد باللغة العربية: {text}"
    try:
        # قمنا بتقليل المهلة لضمان عدم تعليق السكريبت
        response = requests.post(OLLAMA_URL, json={
            "model": "llama3", 
            "prompt": prompt,
            "stream": False
        }, timeout=15)
        
        if response.status_code == 200:
            analysis = response.json().get("response", "").strip()
            return analysis if analysis else "تم استلام رد فارغ من AI."
        else:
            return f"خطأ في محرك AI (كود {response.status_code})"
    except Exception as e:
        return "⚠️ محرك AI غير مستعد حالياً (تأكد من تشغيل Ollama في Docker)."

def send_telegram_safe(msg):
    """إرسال الرسالة مع حماية ضد أخطاء التنسيق"""
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    
    # المحاولة الأولى: تنسيق Markdown (الأنيق)
    payload = {"chat_id": CHAT_ID, "text": msg, "parse_mode": "Markdown"}
    res = requests.post(url, json=payload)
    
    # إذا فشلت (بسبب رموز خاصة من AI)، نرسلها كنص عادي (PlainText)
    if res.status_code != 200:
        print("⚠️ مشكلة في التنسيق، يتم الإرسال بنمط النص البسيط...")
        payload = {"chat_id": CHAT_ID, "text": msg}
        requests.post(url, json=payload)
    else:
        print("✅ تم إرسال الإشعار بنجاح.")

def run_production_cycle():
    print("🚀 بدء دورة التوثيق الذكي النهائية...")
    
    # 1. إنشاء ملف الاختبار
    ts = datetime.datetime.now().strftime("%H_%M_%S")
    file_name = f"Final_Test_{ts}.txt"
    file_path = os.path.join(VAULT_PATH, file_name)
    
    content = f"وثيقة تجريبية نهائية لنظام Omniverse - طرابلس.\nالتوقيت: {ts}"
    
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(content)
    
    # 2. حساب البصمة (Hash)
    sha256 = hashlib.sha256()
    with open(file_path, "rb") as f:
        while chunk := f.read(4096): sha256.update(chunk)
    file_hash = sha256.hexdigest()

    # 3. الحصول على التحليل (معالجة ذكية)
    ai_analysis = ask_ollama(content)

    # 4. بناء الرسالة
    final_msg = (
        f"✅ *تم التوثيق بنجاح*\n"
        f"━━━━━━━━━━━━━━━\n"
        f"📄 *الملف:* {file_name}\n"
        f"🔐 *البصمة:* `{file_hash}`\n"
        f"🤖 *التحليل:* {ai_analysis}\n"
        f"━━━━━━━━━━━━━━━\n"
        f"📍 نود طرابلس - الريادة للحاسبات"
    )
    
    send_telegram_safe(final_msg)
    print("🏁 اكتملت العملية.")

if __name__ == "__main__":
    run_production_cycle()