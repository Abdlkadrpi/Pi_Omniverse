import requests
import json
import logging

# إعداد السجلات لتتبع حالة الاتصال بين السيرفرين
logging.basicConfig(level=logging.INFO, format="%(asctime)s - [Omniverse-Bridge] - %(levelname)s - %(message)s")

TRIPOLI_NODE_URL = "http://127.0.0.1:5000/api/v1/route-fees"

def send_transaction_to_tripoli_node(transaction_id: str, fee_amount: float):
    """
    يقوم بإرسال تفاصيل المعاملة والرسوم من تطبيق أومنيفيرس (المنفذ 10000) 
    إلى عقدة طرابلس (المنفذ 5000) لتوزيعها وحمايتها بتشفير PQC.
    """
    payload = {
        "transaction_id": transaction_id,
        "fee_amount": fee_amount
    }
    
    headers = {
        "Content-Type": "application/json",
        "X-Omniverse-Source": "App-Server-Port-10000"
    }
    
    try:
        logging.info(f"إرسال المعاملة {transaction_id} بقيمة رسوم ${fee_amount} إلى عقدة طرابلس...")
        response = requests.post(TRIPOLI_NODE_URL, json=payload, headers=headers, timeout=5)
        
        if response.status_code == 200:
            result = response.json()
            logging.info("✔️ تم بنجاح استلام وتوزيع الرسوم من قبل عقدة طرابلس!")
            return result
        else:
            logging.error(f"❌ فشل الاستجابة من العقدة برمز الخطأ {response.status_code}: {response.text}")
            return {"success": False, "error": response.text}
            
    except requests.exceptions.ConnectionError:
        logging.error("❌ تعذر الاتصال بعقدة طرابلس على المنفذ 5000. تأكد من أن سيرفر العقدة يعمل!")
        return {"success": False, "error": "Connection Refused to Tripoli Node"}
    except Exception as e:
        logging.error(f"❌ حدث خطأ غير متوقع أثناء ربط السيرفرين: {str(e)}")
        return {"success": False, "error": str(e)}

# اختبار اتصال وتجربة إرسال معاملة فورية عند التشغيل
if __name__ == "__main__":
    test_res = send_transaction_to_tripoli_node("TEST_OMNI_LIVE_007", 0.10)
    print(json.dumps(test_res, indent=4, ensure_ascii=False))