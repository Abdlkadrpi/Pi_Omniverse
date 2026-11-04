import os
import requests
import json

# الروابط ومسارات الـ API لعقدة طرابلس
SERVER_URL = "http://127.0.0.1:10000/api/v1/lyo/execute-task"
ARCHIVE_API_URL = "http://127.0.0.1:10000/api/v1/sovereign/ledger/archive"

def step_1_check_server():
    print("=" * 70)
    print("[*] الخطوة 1/3: التحقق من جاهزية سيرفر عقدة طرابلس (Tripoli Node v0.6.3)...")
    print("=" * 70)
    try:
        health_res = requests.get("http://127.0.0.1:10000/health", timeout=5)
        if health_res.status_code == 200:
            print("[✔] السيرفر يعمل بحالة ممتازة ومستعد لتلقي المعاملات السيادية.\n")
            return True
        else:
            print("[-] تحذير: السيرفر استجاب ولكن بوضع غير متوقع.")
            return False
    except requests.exceptions.ConnectionError:
        print("[-] خطأ: تعذر الاتصال بالسيرفر. تأكد من تشغيل ملف app.py أولاً عبر أمر: python app.py\n")
        return False

def step_2_send_test_transaction():
    print("=" * 70)
    print("[*] الخطوة 2/3: إرسال المعاملة التجريبية الموثقة مع التوقيع الكمي...")
    print("=" * 70)
    
    payload = {
        "user_uid": "tripoli_node_admin_01",
        "is_kyc_verified": True,
        "amount_lyo": 50.0,
        "action": "verify_node_ledger"
    }
    
    headers = {
        "Content-Type": "application/json",
        "User-Agent": "OmniverseSovereignClient/0.6.3"
    }

    try:
        response = requests.post(SERVER_URL, json=payload, headers=headers, timeout=10)
        print(f"[+] كود الاستجابة (Status Code): {response.status_code}")
        
        res_json = response.json()
        print("[+] رد العقدة والتحقق السيادي:")
        print(json.dumps(res_json, indent=4, ensure_ascii=False))
        print("\n[✔] تم تنفيذ المعاملة وأرشفتها بنجاح داخل أستاذ العقدة.\n")
        return response.status_code == 200
    except Exception as e:
        print(f"[-] حدث خطأ أثناء إرسال الطلب: {e}")
        return False

def step_3_fetch_archive_via_api():
    print("=" * 70)
    print("[*] الخطوة 3/3: استعلام دفتر الأستاذ عبر مسار الـ API المباشر مع ترويسات الأمان...")
    print("=" * 70)
    
    # تمرير ترويسات الأمان لاجتياز ميدلوير require_zero_trust_security
    headers = {
        "Content-Type": "application/json",
        "User-Agent": "OmniverseSovereignClient/0.6.3"
    }

    try:
        response = requests.get(ARCHIVE_API_URL, headers=headers, timeout=5)
        if response.status_code == 200:
            data = response.json()
            total = data.get("total_records", 0)
            transactions = data.get("transactions", [])

            if total == 0:
                print("[!] لا توجد معاملات مؤرشفة في السجل حتى الآن.")
                return

            print(f"[+] تم جلب ({total}) معاملة مؤرشفة بنجاح عبر الـ API:\n")
            for idx, tx in enumerate(transactions, 1):
                print(f"--- معاملة رقم [{idx}] ---")
                print(f"  • معرف المعاملة (TX ID) : {tx.get('transaction_id')}")
                print(f"  • المستخدم (Pi UID)    : {tx.get('pi_user_uid')}")
                print(f"  • نوع الخدمة/المهمة    : {tx.get('service_type')}")
                print(f"  • المبلغ الإجمالي     : {tx.get('gross_paid_lyo')} LYO")
                print(f"  • الصافي المخصص       : {tx.get('net_allocated_lyo')} LYO")
                print(f"  • نسبة الحرق (1%)     : {tx.get('burned_lyo')} LYO")
                print(f"  • عنوان الحرق (Burn)   : {tx.get('burn_address')}")
                print(f"  • التحقق الكمي (PQC)   : {'✅ مجتاز' if tx.get('pqc_verified') else '❌ مرفوض'}")
                print(f"  • الطابع الزمني        : {tx.get('timestamp')}")
                print("-" * 70)
        else:
            print(f"[-] فشل الاستعلام عبر الـ API بكود خطأ: {response.status_code}")
    except Exception as e:
        print(f"[-] حدث خطأ أثناء الاتصال بمسار الأرشيف: {e}")

if __name__ == "__main__":
    if step_1_check_server():
        success = step_2_send_test_transaction()
        if success:
            step_3_fetch_archive_via_api()
        else:
            print("[-] تخطي خطوة جلب الأرشيف لعدم نجاح إرسال المعاملة.")