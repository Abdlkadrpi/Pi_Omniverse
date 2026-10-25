import hmac
import hashlib
import time
import requests
import json

# الإعدادات المحلية
SERVER_URL = "http://127.0.0.1:10000/api/v1/lyo/execute-utility"
SECRET_GUARD_KEY = b"OMNIVERSE_TRIPOLI_NODE_SECURE_HMAC_KEY_2026"

def test_secure_lyo_utility():
    # 1. تجهيز بيانات الطلب (Payload) المتوافقة مع معايير المنفعة
    payload = {
        "pi_user_uid": "test_sovereign_user_123",
        "service_type": "notary_service",
        "amount": 150.0
    }
    
    body_string = json.dumps(payload)
    timestamp = str(int(time.time()))
    
    # 2. توليد التوقيع التشفيري الأمني (HMAC-SHA256)
    message_to_sign = body_string.encode('utf-8') + timestamp.encode('utf-8')
    signature = hmac.new(SECRET_GUARD_KEY, message_to_sign, hashlib.sha256).hexdigest()
    
    # 3. تجهيز الترويسات الأمنية (Headers)
    headers = {
        "Content-Type": "application/json",
        "X-Omniverse-Timestamp": timestamp,
        "X-Omniverse-Signature": signature
    }
    
    print("[*] جاري إرسال الطلب الآمن لعملة LYO إلى الخادم المحلي...")
    
    try:
        # 4. إرسال طلب POST الآمن
        response = requests.post(SERVER_URL, data=body_string, headers=headers, timeout=5)
        
        print(f"\n[+] رمز الاستجابة (Status Code): {response.status_code}")
        print("[+] محتوى الاستجابة من الخادم:")
        print(json.dumps(response.json(), indent=4, ensure_ascii=False))
        
    except requests.exceptions.ConnectionError:
        print("[-] خطأ: تعذر الاتصال بالسيرفر. تأكد من أن تطبيق app.py يعمل على المنفذ 10000.")
    except Exception as e:
        print(f"[-] حدث خطأ غير متوقع: {str(e)}")

if __name__ == "__main__":
    test_secure_lyo_utility()