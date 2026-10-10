import requests
import os

def check_pi_validation():
    # الرابط الخاص بك
    url = "https://pi-omniverse-1.onrender.com/.well-known/pi-domain-validation.txt"
    # الكود الذي يجب أن يظهر
    expected_key = "112071584851e3e7a9cebf5cc5d"
    
    print(f"--- فحص رابط التوثيق: {url} ---")
    
    try:
        response = requests.get(url, timeout=10)
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 200:
            content = response.text.strip()
            print(f"Content Found: {content}")
            
            if expected_key in content:
                print("✅ النتيجة: التوثيق صحيح تماماً ومطابق للمطلوب!")
                print("نصيحة: المشكلة في بوابة Pi نفسها، انتظر 15 دقيقة ثم حاول الضغط على Continue مرة أخرى.")
            else:
                print("❌ النتيجة: المحتوى غير مطابق للكود المتوقع!")
        else:
            print("❌ النتيجة: الرابط لا يعمل، تأكد من أن السيرفر يعمل على Render.")
            
    except Exception as e:
        print(f"خطأ في الاتصال: {e}")

if __name__ == "__main__":
    check_pi_validation()