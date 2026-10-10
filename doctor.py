import urllib.request
import json
import time
import sys

BASE_URL = "http://127.0.0.1:10000"

def test_endpoint(path, method="GET"):
    url = BASE_URL + path
    print(f"[*] Testing [{method}] {url} ...")
    try:
        req = urllib.request.Request(url, method=method)
        with urllib.request.urlopen(req, timeout=5) as response:
            data = response.read().decode('utf-8')
            print(f"[+] Success! Status: {response.status}")
            try:
                print(json.dumps(json.loads(data), indent=2, ensure_ascii=False))
            except:
                print(data)
            return True
    except Exception as e:
        print(f"[-] Error connecting to {path}: {e}")
        return False

if __name__ == "__main__":
    print("=== Omniverse System Doctor & Diagnostics ===")
    time.sleep(1)
    
    # 1. اختبار حالة العقدة
    if not test_endpoint("/api/node/status"):
        print("[-] Server is not responding. Please make sure 'python app.py' is running in another terminal.")
        sys.exit(1)
        
    # 2. تشغيل معاملات الاختبار والتجربة
    print("\n--- Triggering Test Payments ---")
    test_endpoint("/trigger-test-payments")
    
    # 3. فحص قاعدة البيانات والأصول المسجلة
    print("\n--- Checking Database Transactions ---")
    test_endpoint("/api/check-transactions")
    
    print("\n[+] Diagnostics completed successfully!")