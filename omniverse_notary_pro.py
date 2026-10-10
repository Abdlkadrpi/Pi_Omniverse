import hashlib
import os
import time
import requests
from datetime import datetime

# --- الإعدادات ---
TOKEN = "8689618232:AAFIF8XzxpxnYfg37-vIJhKHYntUrvjB5sc"
CHAT_ID = "6043063504"
WATCH_DIR = r"C:\Users\الريادة للحاسبات\Desktop\Omniverse\Omniverse_Notary_Vault"
OLLAMA_URL = "http://localhost:11434/api/generate" # رابط Ollama المحلي

def ask_ollama(text_content):
    """استشارة الذكاء الاصطناعي Ollama حول محتوى الوثيقة"""
    prompt = f"قم بتلخيص هذه الوثيقة في سطر واحد فقط باللغة العربية: {text_content[:500]}"
    try:
        response = requests.post(OLLAMA_URL, json={
            "model": "llama3", # أو الموديل الذي قمت بتحميله
            "prompt": prompt,
            "stream": False
        })
        return response.json().get("response", "لم يتمكن الذكاء الاصطناعي من التحليل.")
    except:
        return "محرك الذكاء الاصطناعي Ollama غير متاح حالياً."

def send_telegram_msg(message):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    payload = {"chat_id": CHAT_ID, "text": message, "parse_mode": "Markdown"}
    requests.post(url, json=payload)

def hash_file(file_path):
    sha256 = hashlib.sha256()
    with open(file_path, "rb") as f:
        while chunk := f.read(4096): sha256.update(chunk)
    return sha256.hexdigest()

print(f"🧠 الوكيل الموثق الذكي (AI) يعمل الآن...")

processed_files = set(os.listdir(WATCH_DIR))

while True:
    current_files = os.listdir(WATCH_DIR)
    for file in current_files:
        file_path = os.path.join(WATCH_DIR, file)
        if file not in processed_files and os.path.isfile(file_path):
            file_hash = hash_file(file_path)
            
            # قراءة محتوى الملف إذا كان نصياً لتحليله
            ai_summary = "ملف غير نصي (سيتم توثيق البصمة فقط)."
            if file.endswith('.txt'):
                with open(file_path, 'r', encoding='utf-8') as f:
                    ai_summary = ask_ollama(f.read())

            msg = (
                f"📑 *توثيق ذكي جديد - Omniverse AI*\n"
                f"━━━━━━━━━━━━━━━\n"
                f"📄 *الملف:* `{file}`\n"
                f"🔐 *البصمة:* `{file_hash}`\n"
                f"🤖 *تحليل AI:* {ai_summary}\n"
                f"⏰ *التوقيت:* {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
                f"━━━━━━━━━━━━━━━\n"
                f"✅ تم التحليل والتوثيق بنجاح."
            )
            
            send_telegram_msg(msg)
            processed_files.add(file)
            print(f"✅ تم توثيق وتحليل {file}")
            
    time.sleep(5)