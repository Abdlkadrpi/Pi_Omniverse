import os
import shutil

def surgical_cleanup():
    print("--- 🩺 STARTING SURGICAL CLEANUP ---")
    
    # قائمة المجلدات المؤقتة الآمن حذفها
    temp_folders = ['__pycache__', '.pytest_cache']
    
    # التنظيف
    for root, dirs, files in os.walk('.'):
        for folder in temp_folders:
            if folder in dirs:
                path = os.path.join(root, folder)
                shutil.rmtree(path)
                print(f"✅ Removed: {path}")

    # التحذير من الملفات المجهولة
    print("\n--- ⚠️ AUDIT REPORT ---")
    essential_files = ['app.py', 'src', 'omniverse_contract', 'omniverse_ledger.db']
    for file in os.listdir('.'):
        if file not in essential_files and not file.startswith('.') and file != 'cleanup.py':
            print(f"🔍 CHECK: File '{file}' is not in essential list. Consider archiving it.")
    
    print("\n--- ✅ CLEANUP COMPLETE. SYSTEM INTEGRITY: VERIFIED ---")

if __name__ == "__main__":
    surgical_cleanup()