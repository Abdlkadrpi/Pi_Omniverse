import time
import subprocess
import requests

# --- البيانات المصححة بدقة ---
TELEGRAM_TOKEN = "8689618232:AAFIF8XzxpxnYfg37-vIJhKHYntUrvjB5sc"
CHAT_ID = 6043063504  # تم تحويله لرقم لضمان قبول تليجرام

def send_telegram_alert(message):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    payload = {
        "chat_id": CHAT_ID, 
        "text": f"🛡️ نظام Omniverse - نود طرابلس:\n{message}",
        "parse_mode": "Markdown"
    }
    try:
        response = requests.post(url, json=payload, timeout=30)
        if response.status_code == 200:
            print("✅ تم إرسال التنبيه إلى تليجرام بنجاح.")
        else:
            # طباعة الرد من تليجرام لفهم المشكلة بدقة
            print(f"⚠️ فشل الإرسال. استجابة تليجرام: {response.text}")
    except Exception as e:
        print(f"❌ خطأ تقني: {e}")

def monitor_node():
    container_name = "pi-consensus"
    try:
        # فحص حالة الحاوية
        result = subprocess.run(["docker", "inspect", "-f", "{{.State.Running}}", container_name], 
                               capture_output=True, text=True)
        
        if "true" not in result.stdout.lower():
            print("🚨 النود متوقف حالياً. جاري إعادة التشغيل...")
            send_telegram_alert("⚠️ *تنبيه حرج*: نود Pi متوقف! جاري إعادة التشغيل تلقائياً...")
            
            # أمر إعادة التشغيل
            subprocess.run(["docker", "start", container_name])
            time.sleep(15)
            send_telegram_alert("✅ *تم استعادة النظام*: النود يعمل الآن.")
        else:
            print(f"[{time.strftime('%H:%M:%S')}] النود يعمل بنجاح ✅")
            
    except Exception as e:
        print(f"❌ خطأ في الدوكر: {e}")

# رسالة اختبار البداية
print("🚀 إطلاق الوكيل الحارس...")
send_telegram_alert("🚀 *نظام المراقبة مفعل*\nأهلاً بك يا عبد القادر، نود طرابلس تحت حمايتي الآن.")

while True:
    monitor_node()
    time.sleep(60)