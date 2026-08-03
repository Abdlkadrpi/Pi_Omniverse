import time
import requests
from concurrent.futures import ThreadPoolExecutor

# إعدادات السيرفر المحلي أو السحابي
SERVER_URL = "http://127.0.0.1:10000"
WEBHOOK_ENDPOINT = f"{SERVER_URL}/pi-webhook"

# بيانات تجريبية لمحاكاة طلب دفع أو تحقق (KYC) لـ Pi Network
payload_template = {
    "paymentId": "pi_test_payment_900_files",
    "userUid": "user_smart_city_01",
    "amount": 10.0,
    "status": "COMPLETED"
}

def simulate_request(index):
    start_time = time.time()
    try:
        # محاكاة إرسال طلب تفتيش أو مزامنة سحابية
        response = requests.post(WEBHOOK_ENDPOINT, json=payload_template, timeout=5)
        latency = time.time() - start_time
        return index, response.status_code, latency
    except requests.exceptions.RequestException as e:
        return index, "FAILED", str(e)

def run_load_test(total_requests=50, max_workers=10):
    print(f"[*] بدء اختبار التحمل على: {WEBHOOK_ENDPOINT}")
    print(f"[*] إرسال {total_requests} طلب بمعدل {max_workers} خيوط تنفيذ (Threads) متزامنة...\n")
    
    success_count = 0
    fail_count = 0
    total_latency = 0

    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = [executor.submit(simulate_request, i) for i in range(total_requests)]
        
        for future in futures:
            idx, status, latency = future.result()
            if status == 200 or status == 201:
                success_count += 1
                total_latency += latency
                print(f"[✔] الطلب #{idx+1} نجح | زمن الاستجابة: {latency:.4f} ثانية")
            else:
                fail_count += 1
                print(f"[✘] الطلب #{idx+1} فشل | الحالة: {status}")

    if success_count > 0:
        avg_latency = total_latency / success_count
        print("\n================== نتائج الاختبار ==================")
        print(f" إجمالي الطلبات الناجحة: {success_count}/{total_requests}")
        print(f" إجمالي الطلبات الفاشلة: {fail_count}/{total_requests}")
        print(f" متوسط سرعة التنفيذ واستجابة السيرفر: {avg_latency:.4f} ثانية")
        print("====================================================")

if __name__ == "__main__":
    run_load_test()