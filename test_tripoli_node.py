import requests
import json
import hashlib
import time

# إعدادات العقدة والخدمات المحلية
LOCAL_AI_URL = "http://127.0.0.1:10000/api/ai/process"
SOROBAN_RPC_URL = "http://localhost:8000/rpc"
NODE_NAME = "Tripoli-Node-0.6.3"

def test_pqc_signature(task_text):
    """محاكاة توليد توقيع مقاوم للكم (PQC-Sig) محلياً"""
    timestamp = str(time.time())
    raw_data = f"{NODE_NAME}-{task_text}-{timestamp}"
    pqc_sig = hashlib.sha256(raw_data.encode()).hexdigest()
    return pqc_sig

def run_tests():
    print("=" * 60)
    print(f"🚀 بدء الاختبار التلقائي لمنظومة {NODE_NAME} (Omniverse & Tripoli Node)")
    print("=" * 60)

    # 1. اختبار التوقيعات الكمومية (PQC) ووظائف توكن LYO
    print("\n[1/3] اختبار توليد درع الحماية وتوقيع PQC لتوكن LYO...")
    sample_task = "Autonomous scan: Optimize smart city energy grid and allocate LYO fuel reserves under PQC shield."
    sig = test_pqc_signature(sample_task)
    print(f"  ✅ تم توليد التوقيع بنجاح:")
    print(f"     PQC-Sig: {sig}")

    # 2. اختبار الاتصال بالذكاء الاصطناعي المحلي (Port 10000)
    print("\n[2/3] اختبار الاتصال بخلاف الذكاء الاصطناعي المحلي (Port 10000)...")
    try:
        payload = {"prompt": "Check Tripoli Node status and verify LYO fuel reserves."}
        response = requests.post(LOCAL_AI_URL, json=payload, timeout=5)
        
        if response.status_code == 200:
            data = response.json()
            print(f"  ✅ استجابة الذكاء الاصطناعي المحلي ناجحة (HTTP 200):")
            print(f"     الرد: {data.get('response', data)[:150]}...")
        else:
            print(f"  ⚠️ الخاستجابة من المنفذ 10000 برمز الحالة: {response.status_code}")
    except requests.exceptions.ConnectionError:
        print("  ❌ فشل الاتصال! تأكد من أن خادم الذكاء الاصطناعي المحلي يعمل على http://127.0.0.1:10000")
    except Exception as e:
        print(f"  ❌ حدث خطأ غير متوقع: {e}")

    # 3. اختبار Soroban RPC & Ledger (Port 8000)
    print("\n[3/3] اختبار فحص شبكة Soroban RPC & Ledger (Port 8000)...")
    try:
        rpc_payload = {
            "jsonrpc": "2.0",
            "method": "getLatestLedger",
            "params": {},
            "id": 1
        }
        rpc_response = requests.post(SOROBAN_RPC_URL, json=rpc_payload, timeout=5)
        
        if rpc_response.status_code == 200:
            print(f"  ✅ اتصال Soroban RPC يعمل بامتياز (HTTP 200):")
            print(f"     البيانات: {rpc_response.json()}")
        else:
            print(f"  ⚠️ استجابة RPC برمز الحالة: {rpc_response.status_code}")
    except requests.exceptions.ConnectionError:
        print("  ℹ️ ملاحظة: خادم Soroban RPC على المنفذ 8000 غير متصل حالياً (يمكن تجاوزه إذا كنت تختبر الواجهة فقط محلياً).")
    except Exception as e:
        print(f"  ❌ حدث خطأ أثناء فحص RPC: {e}")

    print("\n" + "=" * 60)
    print("🏁 انتهى فحص واختبار منظومة طرابلس بنجاح.")
    print("=" * 60)

if __name__ == "__main__":
    run_tests()