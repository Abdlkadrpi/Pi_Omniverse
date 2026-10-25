import requests
import json

# عنوان جسر نود طرابلس المحلي على المنفذ 5000
TRIPOLI_NODE_URL = "http://127.0.0.1:5000/api/node/status"
# عنوان سيرفر التطبيق المحلي على المنفذ 10000
APP_ENGINE_URL = "http://127.0.0.1:10000/api/node/status"

def test_bridge_connectivity():
    print("[*] جاري فحص الاتصال المباشر مع نود طرابلس (المنفذ 5000)...")
    try:
        res_node = requests.get(TRIPOLI_NODE_URL, timeout=3)
        if res_node.status_code == 200:
            print("[+] نود طرابلس متصل ويستجيب بنجاح:")
            print(json.dumps(res_node.json(), indent=4, ensure_ascii=False))
        else:
            print(f"[-] نود طرابلس استجاب برمز خطأ: {res_node.status_code}")
    except requests.exceptions.ConnectionError:
        print("[-] تنبيه: نود طرابلس غير عامل حالياً على المنفذ 5000 (يعمل التطبيق في وضع الاستقلالية المحلي).")

    print("\n[*] جاري فحص مسار جسر النود في سيرفر التطبيق (المنفذ 10000)...")
    try:
        res_app = requests.get(APP_ENGINE_URL, timeout=3)
        if res_app.status_code == 200:
            print("[+] استجابة سيرفر التطبيق بنجاح:")
            print(json.dumps(res_app.json(), indent=4, ensure_ascii=False))
        else:
            print(f"[-] سيرفر التطبيق استجاب برمز خطأ: {res_app.status_code}")
    except requests.exceptions.ConnectionError:
        print("[-] خطأ: تأكد من تشغيل سيرفر app.py على المنفذ 10000.")

if __name__ == "__main__":
    test_bridge_connectivity()