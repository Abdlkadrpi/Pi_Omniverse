import os
import hashlib

def get_file_hash(filepath):
    """حساب بصمة الملف للتأكد من أنه مكرر فعلياً"""
    hasher = hashlib.md5()
    with open(filepath, 'rb') as f:
        buf = f.read()
        hasher.update(buf)
    return hasher.hexdigest()

def find_duplicates(root_dir):
    hashes = {}
    duplicates = []
    
    print(f"🔍 Scanning: {root_dir} for duplicates...\n")
    
    for dirpath, _, filenames in os.walk(root_dir):
        # تجاهل مجلدات النظام والبيانات
        if 'venv' in dirpath or '.git' in dirpath or 'omniverse_ledger.db' in dirpath:
            continue
            
        for filename in filenames:
            filepath = os.path.join(dirpath, filename)
            file_hash = get_file_hash(filepath)
            
            if file_hash in hashes:
                duplicates.append((filepath, hashes[file_hash]))
            else:
                hashes[file_hash] = filepath
                
    return duplicates

if __name__ == '__main__':
    base_path = os.getcwd()
    dups = find_duplicates(base_path)
    
    if dups:
        print("🚨 Found duplicates:")
        for dup, original in dups:
            print(f"Duplicate: {dup}")
            print(f"Original:  {original}")
            print("-" * 30)
        print("\n💡 نصيحة: انسخ مسارات الملفات التي تريد حذفها واستخدم أمر: del 'مسار_الملف'")
    else:
        print("✅ No duplicate files found!")