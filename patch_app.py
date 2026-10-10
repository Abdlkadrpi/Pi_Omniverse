import os

patch_content = """
# 5. معالجة الملفات الثابتة مع دعم المسارات القانونية
@app.route('/<path:path>')
def serve_static(path):
    # إذا كان الطلب لملف الـ legal، تأكد من فتحه مباشرة
    if path == 'legal.html':
        return send_from_directory(UI_DIR, 'legal.html')
        
    # تنظيف المسار
    clean_path = path.replace('ui/', '', 1)
    
    # تحقق مما إذا كان الملف موجوداً فعلياً قبل إرجاعه
    if os.path.exists(os.path.join(UI_DIR, clean_path)):
        return send_from_directory(UI_DIR, clean_path)
    
    return send_from_directory(UI_DIR, 'index.html')
"""

def patch_app_file():
    file_path = 'app.py'
    with open(file_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    # حذف الدالة القديمة وإضافة الجديدة (بافتراض أنها في نهاية الملف)
    # نقوم بالبحث عن السطر الذي يبدأ بـ @app.route('/<path:path>')
    new_lines = []
    skip = False
    for line in lines:
        if "@app.route('/<path:path>')" in line:
            skip = True
        if skip and line.startswith('if __name__ =='):
            skip = False
            new_lines.append(patch_content + "\n" + line)
        elif not skip:
            new_lines.append(line)

    with open(file_path, 'w', encoding='utf-8') as f:
        f.writelines(new_lines)
    print("[+] app.py has been patched successfully.")

if __name__ == "__main__":
    patch_app_file()
"""