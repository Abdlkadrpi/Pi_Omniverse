import hashlib
import os
import requests
import datetime
import subprocess
import shutil

# --- الإعدادات السيادية ---
TOKEN = "8689618232:AAFIF8XzxpxnYfg37-vIJhKHYntUrvjB5sc"
CHAT_ID = "6043063504"
VAULT_PATH = r"C:\Users\الريادة للحاسبات\Desktop\Omniverse\Omniverse_Notary_Vault"
OLLAMA_URL = "http://localhost:11434/api/generate"

def get_system_info():
    """فحص موارد الجهاز (غرفة العمليات)"""
    total, used, free = shutil.disk_usage("C:")
    return f"المساحة المتوفرة: {free // (2**30)} GB من أصل {total // (2**30)} GB"

def check_pi_node():
    """فحص حالة نود Pi Network داخل Docker"""
    try:
        result = subprocess.check_output('docker exec pi-consensus pi-node info', shell=True, stderr=subprocess.STDOUT)
        return "✅ النود متصل ومزامن."
    except:
        return "⚠️ تعذر جلب بيانات النود (تأكد من تشغيل الحاوية)."

def ask_ai_legal(text):
    """اختبار القدرة القانونية لـ TinyLlama"""
    prompt = f"Extract the parties and the amount from this contract in Arabic: {text}"
    try:
        response = requests.post(OLLAMA_URL, json={
            "model": "tinyllama:latest",
            "prompt": prompt,
            "stream": False
        }, timeout=120) # زيادة الوقت لضمان الدقة
        return response.json().get("response", "لم يتم التحليل.")
    except Exception as e:
        return f"خطأ في الاتصال بـ AI: {str(e)}"

def run_strategic_mission():
    print("🚀 بدء المهمة الهندسية الشاملة...")
    
    # 1. إنشاء "عقد عقاري تجريبي" لفحص الذكاء القانوني
    contract_content = """
    عقد بيع عقار رقم 2026/01
    البائع: شركة الريادة للحاسبات - طرابلس
    المشتري: مشروع Omniverse العالمي
    الثمن: 50,000 Pi Coin
    الموضوع: توثيق مقر الابتكار الرقمي في طرابلس.
    """
    
    file_name = "Strategic_Legal_Test.txt"
    file_path = os.path.join(VAULT_PATH, file_name)
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(contract_content)
    
    # 2. العمليات الهندسية
    file_hash = hashlib.sha256(contract_content.encode()).hexdigest()
    sys_info = get_system_info()
    pi_status = check_pi_node()
    ai_analysis = ask_ai_legal(contract_content)
    
    # 3. صياغة التقرير الاستراتيجي للهاتف
    report = (
        f"📊 *تقرير المهمة الاستراتيجية - Omniverse*\n"
        f"━━━━━━━━━━━━━━━\n"
        f"🔍 *اختبار التوثيق القانوني:*\n"
        f"📄 الملف: `{file_name}`\n"
        f"🔐 البصمة: `{file_hash[:20]}...`\n\n"
        f"🤖 *تحليل الذكاء القانوني:*\n"
        f"_{ai_analysis.strip()}_\n\n"
        f"⚙️ *غرفة العمليات (Hardware):*\n"
        f"💾 {sys_info}\n"
        f"🌐 نود Pi: {pi_status}\n"
        f"━━━━━━━━━━━━━━━\n"
        f"📍 المصدر: نود طرابلس السيادي\n"
        f"✅ جاهز للمرحلة التالية."
    )
    
    requests.post(f"https://api.telegram.org/bot{TOKEN}/sendMessage", 
                  json={"chat_id": CHAT_ID, "text": report, "parse_mode": "Markdown"})
    print("🏁 انتهت المهمة. تفقد التقرير الشامل على هاتفك.")

if __name__ == "__main__":
    run_strategic_mission()