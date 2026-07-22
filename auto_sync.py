import os
import time

print("------------------------------------------")
print("🚀 مرحباً بك في نظام مزامنة أومني فيرس (Web3)")
print("------------------------------------------")

# طلب الرابط اليدوي من القائد
public_url = input("🔑 يرجى لصق رابط الـ SSH (الذي ينتهي بـ .lhr.life) هنا: ").strip()

if not public_url:
    print("❌ خطأ: لم تقم بإدخال الرابط!")
    exit()

# التأكد من وجود البروتوكول https
if not public_url.startswith("http"):
    public_url = "https://" + public_url

print(f"⚙️ جاري تحديث ملفات المشروع بالرابط الجديد: {public_url}")

# تحديث رابط الـ API في ملفات HTML (افترضنا أن ملفك اسمه index.html في مجلد ui)
file_path = "ui/index.html"
if os.path.exists(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()
    
    # استبدال أي رابط قديم بالرابط الجديد (تأكد من تسمية المتغير في الـ HTML بـ 'API_URL')
    import re
    new_content = re.sub(r'const API_URL = ".*?";', f'const API_URL = "{public_url}";', content)
    
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(new_content)
    print("✅ تم تحديث الرابط داخل index.html")

# المزامنة مع GitHub
print("☁️ جاري رفع التحديثات إلى GitHub...")
os.system("git add .")
os.system('git commit -m "Update API URL to latest tunnel"')
os.system("git push origin main")

print("------------------------------------------")
print("🏁 تمت المزامنة بنجاح! افتح متصفح باي الآن.")
print("------------------------------------------")