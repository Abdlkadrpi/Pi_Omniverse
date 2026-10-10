import requests
import time

BASE_URL = "https://pi-omniverse-1.onrender.com"
USER = {"username": "TestCitizen_01"}

def run_test():
    print("[*] Starting Surgical Integrity Test...")
    
    # 1. اختبار المصادقة
    print("[1] Testing Authentication...")
    res = requests.post(f"{BASE_URL}/api/pi-auth", json={"accessToken": "MOCK_PI_TOKEN"})
    print(f"[DEBUG] Auth Response: {res.status_code} - {res.text}")
    assert res.status_code == 200, "Auth Failed"
    print("[+] Auth: PASSED")

    # 2. اختبار العقود الذكية (LYO Token Generation)
    print("[2] Testing LYO Smart Contract Execution...")
    # نقوم بإرسال البيانات بتنسيق مطابق تماماً لما يتوقعه السيرفر
    payload = {"content": "Initial LYO Distribution", "username": USER["username"]}
    res = requests.post(f"{BASE_URL}/api/certify", json=payload)
    
    # تصحيح دقيق للخطأ
    print(f"[DEBUG-CERTIFY] Server Response: {res.status_code} - {res.text}")
    
    assert res.status_code == 200, f"Smart Contract Execution Failed with code {res.status_code}"
    
    cert_id = res.json().get("cert_id")
    print(f"[+] Smart Contract: PASSED (TXID: {cert_id})")

    # 3. اختبار وكيل الحوكمة (AI Governance)
    print("[3] Testing AI Governance Audit...")
    res = requests.post(f"{BASE_URL}/api/ai_chat", json={"message": "Audit my LYO balance", "username": USER["username"]})
    assert res.status_code == 200, "AI Governance Failed"
    print("[+] AI Governance: PASSED")

    print("\n[!!!] SYSTEM TEST COMPLETE: 100% OPERATIONAL [!!!]")

if __name__ == "__main__":
    try:
        run_test()
    except Exception as e:
        print(f"\n[!] TEST FAILED: {e}")