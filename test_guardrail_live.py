import requests
import json

# المنفذ النشط لخادم Omniverse App Engine
BASE_URL = "http://127.0.0.1:10000"

def test_live_guardrail_and_approval():
    print("[*] بدء اختبار نظام حماية الوكلاء والتحقق البشري لـ Omniverse على المنفذ 10000...")

    # 1. اختبار إرسال إجراء يحتوي على نمط محظور (رابط خارجي)
    dangerous_payload = {
        "agent_name": "Tripoli_SuperAgent",
        "action_type": "HIGH_VALUE_LYO_TRANSFER",
        "payload": {
            "target": "external_untrusted_api",
            "amount": 500000,
            "note": "تحويل غير مصرح به لجلب رابط خارجي http://malicious-site.com/submit-form"
        }
    }

    print("\n[1] إرسال طلب وكيل يحتوي على محتوى محظور (يجب أن يتم حظره فوراً)...")
    try:
        response = requests.post(f"{BASE_URL}/api/agent/high-value-action", json=dangerous_payload)
        print(f"كود الحالة: {response.status_code}")
        print("استجابة السيرفر:")
        print(json.dumps(response.json(), indent=4, ensure_ascii=False))
    except Exception as e:
        print(f"خطأ في الاتصال: {e}")

    # 2. اختبار طلب وكيل سليم لمعاملة كبرى تتطلب تعليقاً للمراجعة البشرية
    safe_high_value_payload = {
        "agent_name": "Tripoli_SuperAgent",
        "action_type": "HIGH_VALUE_LYO_TRANSFER",
        "payload": {
            "target": "Tripoli_Node_Reserve",
            "amount": 100000,
            "purpose": "إعادة تمويل الوقود التشغيلي لشبكة LYO بنجاح"
        }
    }

    print("\n[2] إرسال طلب معاملة كبرى سليم يستوجب تعليقاً للمراجعة البشرية...")
    try:
        response_safe = requests.post(f"{BASE_URL}/api/agent/high-value-action", json=safe_high_value_payload)
        print(f"كود الحالة: {response_safe.status_code}")
        
        res_json = response_safe.json()
        print("استجابة السيرفر:")
        print(json.dumps(res_json, indent=4, ensure_ascii=False))
        
        if response_safe.status_code == 200 and "approval_id" in res_json:
            approval_id = res_json["approval_id"]
            print(f"\n[3] نجاح الاختبار! تم إيقاف الطلب مؤقتاً ومعرف الاعتماد المؤقت هو: {approval_id}")
            print("الآن توجه إلى واجهة المتصفح (http://127.0.0.1:10000) وستجد الطلب في 'مركز تصديق المدير العام' جاهزاً للاعتماد أو الرفض!")
    except Exception as e:
        print(f"خطأ في معالجة الاستجابة الآمنة: {e}")

if __name__ == "__main__":
    test_live_guardrail_and_approval()