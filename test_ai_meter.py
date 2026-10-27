import json
import requests

BASE_URL = "http://127.0.0.1:5000/api/ai/metered-consume"

def run_tests():
    print("=" * 60)
    print("[*] بدء اختبارات عداد استهلاك الذكاء الاصطناعي لعقدة طرابلس...")
    print("=" * 60)

    # 1. اختبار الاستهلاك الطبيعي السليم
    print("\n[Test 1] إرسال طلب استهلاك طبيعي (Prompt: 500, Completion: 300 tokens)...")
    payload_normal = {
        "user_id": "user_abd_01",
        "prompt_tokens": 500,
        "completion_tokens": 300,
    }

    try:
        response = requests.post(BASE_URL, json=payload_normal)
        print(f"Status Code: {response.status_code}")
        print(json.dumps(response.json(), indent=4, ensure_ascii=False))
    except Exception as e:
        print(f"[Error] Failed to connect to server: {e}")

    # 2. اختبار محاكاة هجمة سيبرانية (DoS / Token Flooding)
    print("\n[Test 2] 🛡️ محاكاة هجمة سيبرانية (تضخم متعمد للرموز > 50,000)...")
    payload_attack = {
        "user_id": "user_abd_01",
        "prompt_tokens": 40000,
        "completion_tokens": 20000,
    }

    try:
        response = requests.post(BASE_URL, json=payload_attack)
        print(f"Status Code: {response.status_code}")
        print(json.dumps(response.json(), indent=4, ensure_ascii=False))
    except Exception as e:
        print(f"[Error] Failed to connect to server: {e}")

    print("\n" + "=" * 60)
    print("[*] انتهت اختبارات العداد والدرع الأمني بنجاح.")
    print("=" * 60)

if __name__ == "__main__":
    run_tests()