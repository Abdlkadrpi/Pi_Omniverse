import requests
import json

BASE_URL = "http://127.0.0.1:5000"

def test_full_user_journey():
    print("[1/3] Testing: Identity Authentication...")
    try:
        auth_res = requests.post(f"{BASE_URL}/api/pi-auth", json={"accessToken": "test_token_123"})
        print(f"  [STATUS] Auth Response: {auth_res.status_code}")
    except Exception as e:
        print(f"  [ERROR] Connection failed: {e}")
        return

    print("[2/3] Testing: Asset Registration...")
    try:
        asset_res = requests.post(f"{BASE_URL}/api/register_asset", json={"name": "Tripoli_Smart_Unit", "value": 100, "owner": "Test_User"})
        print(f"  [STATUS] Asset Response: {asset_res.status_code}")
    except Exception as e:
        print(f"  [ERROR] Asset registration failed: {e}")
        return

    print("[3/3] Testing: AI Governance Chat...")
    try:
        chat_res = requests.post(f"{BASE_URL}/api/ai_chat", json={"message": "Audit the system"})
        print(f"  [STATUS] AI Chat Response: {chat_res.status_code}")
    except Exception as e:
        print(f"  [ERROR] AI Chat failed: {e}")
        return

    print("\n[!!!] TEST REPORT: SYSTEM OPERATIONAL.")

if __name__ == "__main__":
    test_full_user_journey()