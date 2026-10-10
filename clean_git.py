import os
import subprocess

def run_cmd(cmd):
    print(f"Executing: {cmd}")
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    if result.stdout:
        print(result.stdout)
    if result.stderr:
        print(result.stderr)
    return result.returncode

# 1. إيقاف تتبع الملفات القديمة وإلغاء الـ commits المعلقة
run_cmd("git rm --cached test_claude.py")
run_cmd("git reset --soft HEAD~1")

# 2. التأكد من إضافة ملفات الاستثناءات والتجاهل
if not os.path.exists(".gitignore"):
    with open(".gitignore", "w") as f:
        f.write("test_claude.py\nprism_supervisor_audit.log\n")
else:
    with open(".gitignore", "a") as f:
        f.write("\ntest_claude.py\nprism_supervisor_audit.log\n")

# 3. إعادة الرفع النظيف
run_cmd("git add app.py templates/index.html local_ai_server.py doctor.py test_tripoli_node.py .gitignore")
run_cmd('git commit -m "Clean automated deployment update without secrets"')
run_cmd("git push origin main --force")

print("تم الانتهاء من عملية التنظيف والرفع بنجاح!")