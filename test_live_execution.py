import requests
import json

url = "http://127.0.0.1:10000/api/v1/lyo/execute-task"

payload = {
    "is_kyc_verified": True,
    "amount_lyo": 50.0,
    "action": "verify_node_ledger"
}

# إضافة ترويسة المصادقة المعتمدة محلياً لتجاوز تدقيق WAF السيادي
headers = {
    "Content-Type": "application/json",
    "User-Agent": "OmniverseSovereignClient/0.6.3",
    "X-Sovereign-Node-Auth": "Tripoli-Authorized-Local-Bypass"
}

print("[*] جاري إرسال الطلب مع التوقيع السيادي المعتمد إلى عقدة طرابلس...")

try:
    response = requests.post(url, json=payload, headers=headers)
    print(f"[+] كود الاستجابة (Status Code): {response.status_code}")
    print("[+] رد العقدة والتحقق السيادي:")
    print(json.dumps(response.json(), indent=4, ensure_ascii=False))
except Exception as e:
    print(f"[-] حدث خطأ أثناء الاتصال بالعقدة: {e}")