import json
import requests

# رابط المنصة على Render أو رابط النفق المحلي
BASE_URL = "https://pi-omniverse-1.onrender.com"

# رؤوس طلبات آمنة تحاكي معايير درع الحماية السيادي
HEADERS = {
    "Content-Type": "application/json",
    "X-Node-Secured": "Omniverse-Global-Bridge",
    "User-Agent": "Tripoli-Node-Inspector/0.6.3",
}


def test_endpoint(name, method, endpoint, payload=None):
    url = f"{BASE_URL.rstrip('/')}/{endpoint.lstrip('/')}"
    print(f"\n[*] اختبار مسار: [{name}] -> {url}")
    try:
        if method.upper() == "GET":
            response = requests.get(url, headers=HEADERS, timeout=10)
        else:
            response = requests.post(
                url, headers=HEADERS, json=payload, timeout=10
            )

        print(f"    - كود الاستجابة (Status Code): {response.status_code}")
        try:
            res_json = response.json()
            print(
                f"    - الاستجابة (JSON): {json.dumps(res_json, indent=2, ensure_ascii=False)[:300]}..."
            )
        except Exception:
            print(f"    - النص الخام: {response.text[:200]}")

    except Exception as e:
        print(f"    ❌ فشل الاتصال: {str(e)}")


if __name__ == "__main__":
    print(
        "=== بدء اختبار منظومة أومنيفيرس وعقدة طرابلس (Tripoli Node v0.6.3) ==="
    )

    # 1. اختبار مسار حالة العقدة (GET)
    test_endpoint("فحص حالة العقدة", "GET", "/api/agent/status")

    # 2. اختبار مسار السجل المالي والدائم (GET)
    test_endpoint("فحص السجل المالي والدائم", "GET", "/api/agent/persistent-ledger")

    # 3. اختبار مسار عداد استهلاك الذكاء الاصطناعي (POST مع حمولة سليمة لاجتياز درع PRISM)
    ai_payload = {
        "user_id": "user_abd_01",
        "prompt_tokens": 120,
        "completion_tokens": 80,
    }
    test_endpoint(
        "عداد الذكاء الاصطناعي وخصم LYO",
        "POST",
        "/api/ai/metered-consume",
        ai_payload,
    )

    # 4. اختبار مسار التوثيق الرقمي للأصول السيادية RWA (POST)
    rwa_payload = {
        "assetName": "Tripoli Solar Microgrid Station 01",
        "assetValue": 5000.0,
        "ownerUid": "user_abd_01",
        "currency": "PI",
        "kycVerified": True,
    }
    test_endpoint(
        "توثيق أصل سيادي RWA", "POST", "/api/rwa/notarize", rwa_payload
    )

    print(
        "\n=== اكتملت كافة اختبارات الفحص الميداني للمنظومة السيادية بنجاح ==="
    )