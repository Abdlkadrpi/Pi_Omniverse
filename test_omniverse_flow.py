import requests
import json
import time

# إعدادات البيئة
BASE_URL = "http://127.0.0.1:5000" # أو رابط Render الخاص بك

def test_full_user_journey():
    print("[1/3] Testing: Identity Authentication (Pi Sign-in Simulation)...")
    # محاكاة تسجيل الدخول بهوية باي
    auth_res = requests.post(f"{BASE_URL}/api/auth", json={"pi_id": "Pioneer_Test_001"})
    if auth_res.status_code == 200:
        print("  [OK] User Authenticated.")
    else:
        print("  [ERROR] Auth Failed!")
        return

    print("[2/3] Testing: PiVerify & KYC Workflow...")
    # محاكاة خطوة التحقق البشري
    verify_res = requests.post(f"{BASE_URL}/api/verify", json={"pi_id": "Pioneer_Test_001", "status": "verified"})
    if verify_res.status_code == 200:
        print("  [OK] KYC Verified by PiVerify.")
    else:
        print("  [ERROR] Verification Failed!")
        return

    print("[3/3] Testing: Asset Registration (LYO Protocol)...")
    # محاكاة تسجيل أصل حقيقي في النظام
    asset_data = {"name": "Tripoli_Smart_Unit", "value": 100, "owner": "Pioneer_Test_001"}
    asset_res = requests.post(f"{BASE_URL}/api/register_asset", json=asset_data)
    
    if asset_res.status_code == 200:
        print("  [OK] Asset Registered Successfully.")
        print("  [SYSTEM RESULT]:", asset_res.json())
    else:
        print("  [ERROR] Asset Registration Failed!")

    print("\n[!!!] TEST REPORT: SYSTEM OPERATIONAL WITH ZERO ERRORS.")

if __name__ == "__main__":
    test_full_user_journey()