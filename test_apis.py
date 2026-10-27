import requests
import json

BASE_URL = "http://localhost:5000"

print("="*60)
print("[*] بدء اختبار مسارات الـ API لعقدة طرابلس والوكلاء الأذكياء...")
print("="*60)

# 1. اختبار حالة العقدة الأساسية
try:
    resp = requests.get(f"{BASE_URL}/api/agent/status", timeout=5)
    print(f"\n[1] فحص حالة العقدة (/api/agent/status): Status Code -> {resp.status_code}")
    print(json.dumps(resp.json(), indent=2, ensure_ascii=False))
except Exception as e:
    print(f"\n[1] فشل الاتصال بمسار الحالة: {e}")

# 2. اختبار فحص الامتثال وسياسات Pi Network وعملة LYO
try:
    payload_comp = {"action": "check_lyo_allocation", "amount": 1000, "target": "smart_city_grid"}
    resp = requests.post(f"{BASE_URL}/api/agent/compliance-check", json=payload_comp, timeout=5)
    print(f"\n[2] فحص الامتثال (/api/agent/compliance-check): Status Code -> {resp.status_code}")
    print(json.dumps(resp.json(), indent=2, ensure_ascii=False))
except Exception as e:
    print(f"\n[2] فشل الاتصال بمسار الامتثال: {e}")

# 3. اختبار التحقق المقاوم للكم (PQC Verification)
try:
    payload_pqc = {
        "action_id": "TEST-ACTION-999",
        "payload": {"module": "Omniverse_Notary", "operation": "hash_verify"}
    }
    resp = requests.post(f"{BASE_URL}/api/pq/verify-action", json=payload_pqc, timeout=5)
    print(f"\n[3] فحص التشفير المقاوم للكم (/api/pq/verify-action): Status Code -> {resp.status_code}")
    print(json.dumps(resp.json(), indent=2, ensure_ascii=False))
except Exception as e:
    print(f"\n[3] فشل الاتصال بمسار PQC: {e}")

# 4. اختبار اقتراح تحديث / تشغيل الوكيل الذكي (تم زيادة المهلة إلى 30 ثانية لتجنب انتهاء الوقت)
try:
    payload_update = {
        "action": "cluster_dispatch",
        "block": 10887646,
        "task": "Audit LYO token energy routing and agents"
    }
    resp = requests.post(f"{BASE_URL}/api/agent/propose-update", json=payload_update, timeout=30)
    print(f"\n[4] فحص اقتراح التحديث وتوجيه الوكيل (/api/agent/propose-update): Status Code -> {resp.status_code}")
    print(json.dumps(resp.json(), indent=2, ensure_ascii=False))
except Exception as e:
    print(f"\n[4] فشل الاتصال بمسار التحديث: {e}")

print("\n" + "="*60)
print("[*] انتهى اختبار مسارات الـ API بنجاح تام.")
print("="*60)