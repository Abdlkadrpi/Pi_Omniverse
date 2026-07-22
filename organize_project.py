import os
import shutil

# قائمة المجلدات المستهدفة
dirs = ['src', 'notary', 'agents', 'contracts', 'ui']
for d in dirs:
    os.makedirs(d, exist_ok=True)

# خريطة نقل الملفات (المصدر -> الوجهة)
mapping = {
    'Omniverse_Final_Notary': 'notary/',
    'Master_AI_Test': 'agents/',
    'omniverse_contract': 'contracts/',
    # انقل باقي ملفاتك هنا بنفس الطريقة
}

for src, dest in mapping.items():
    if os.path.exists(src):
        if os.path.isdir(src):
            shutil.move(src, dest)
        else:
            shutil.move(src, dest + src)
            
print("تم تنظيم المجلدات بنجاح!")