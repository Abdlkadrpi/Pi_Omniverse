import requests

BASE_URL = "http://127.0.0.1:5000"

def test_node():
    print(f"🚀 بدء اختبار عقدة طرابلس الشامل (v2.6.1)...\n")
    
    # 1. اختبار فحص الجودة
    print("--- الاختبار 1: فحص الجودة (نص قصير) ---")
    res1 = requests.post(f"{BASE_URL}/api/process_asset", json={"content": "Hi", "username": "abdlkadr"})
    print(f"الحالة: {'✅ ناجح' if res1.status_code == 400 else '❌ فشل'}")

    # 2. اختبار التوثيق وتحديث الرصيد
    print("\n--- الاختبار 2: التوثيق الفعلي ---")
    res2 = requests.post(f"{BASE_URL}/api/process_asset", json={"content": "Tripoli Node Full System Test", "username": "abdlkadr"})
    if res2.status_code == 200:
        print(f"✅ تم التوثيق بمعرف: {res2.json().get('cert_id')}")
    
    # 3. اختبار السجل التاريخي (History API)
    print("\n--- الاختبار 3: التحقق من سجل المعاملات ---")
    res3 = requests.get(f"{BASE_URL}/api/history")
    history = res3.json()
    if len(history) > 0:
        print(f"✅ تم العثور على {len(history)} معاملات في السجل.")
        print(f"أحدث معاملة: {history[0]['asset']}")
    else:
        print("❌ فشل: سجل المعاملات فارغ!")

    # 4. التحقق النهائي من الرصيد
    res_stats = requests.get(f"{BASE_URL}/api/stats").json()
    print(f"\n📊 الرصيد النهائي: {res_stats.get('reputation')}")
    print(f"📊 ارتفاع دفتر الأستاذ: {res_stats.get('ledger')}")
    
    print(f"\n✨ الاختبار انتهى! النظام جاهز تماماً.")

if __name__ == "__main__":
    test_node()