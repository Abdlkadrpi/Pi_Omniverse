import hashlib
import datetime
import os

# --- إعدادات الهوية السيادية (مستخرجة من نود طرابلس) ---
# مفتاح النود العام الذي استخرجناه من لقطة الشاشة
NODE_ID = "GASOJABWJR2YZBCOBRXWTU2L62FUFNHK57U2LVFABY4W4NL6L25CTYLB"

# المسار الجديد لملف سجل الأصول داخل المجلد الفرعي المنظم
FILE_TO_SIGN = r"C:\Users\الريادة للحاسبات\Desktop\Pi_Omniverse\Omniverse\Asset_Registry.txt"

def generate_sovereign_seal():
    print("🚀 جاري بدء عملية التوثيق السيادي للأصول...")
    
    # 1. التأكد من وجود الملف قبل البدء
    if not os.path.exists(FILE_TO_SIGN):
        print(f"❌ خطأ: لم يتم العثور على الملف في المسار: {FILE_TO_SIGN}")
        return

    try:
        # 2. قراءة محتوى سجل الأصول
        with open(FILE_TO_SIGN, "rb") as f:
            content = f.read()
        
        # 3. توليد البصمة الرقمية للملف (SHA-256)
        doc_hash = hashlib.sha256(content).hexdigest()
        
        # 4. دمج بصمة الملف مع هوية النود لإنشاء الختم النهائي
        combined_data = NODE_ID + doc_hash
        sovereign_seal = hashlib.sha256(combined_data.encode()).hexdigest()
        
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        # 5. عرض تقرير التوثيق النهائي
        print("\n" + "="*40)
        print("--- OMNIVERSE SOVEREIGN SEAL ---")
        print(f"زمان التوثيق : {timestamp}")
        print(f"هوية النود (Tripoli) : {NODE_ID[:15]}...")
        print(f"بصمة المستند الأصلية : {doc_hash[:15]}...")
        print(f"الختم السيادي النهائي : {sovereign_seal}")
        print("="*40)
        
        print("\n✅ تم إنتاج الختم بنجاح. انسخ 'الختم السيادي النهائي' وأرسله لي.")
        
    except Exception as e:
        print(f"❌ حدث خطأ أثناء المعالجة: {str(e)}")

if __name__ == "__main__":
    generate_sovereign_seal()