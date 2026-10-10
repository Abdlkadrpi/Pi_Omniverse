#!/bin/bash

# المسار إلى مجلد المشروع
echo "بدء عملية التنظيف والرفع التلقائي..."

# 1. إزالة الملفات التي تسبب مشاكل في الويندوز (مثل ملفات nul المحجوزة)
find . -name "nul" -type f -delete
find . -name "NUL" -type f -delete

# 2. حذف المجلدات غير الضرورية التي لا نحتاجها في السحابة
rm -rf venv/ target/ __pycache__/ .env

# 3. تجهيز الملفات للرفع
git add .

# 4. تأكيد التغييرات
git commit -m "Auto-deploy: Cleanup and structural update $(date)"

# 5. الرفع إلى GitHub
git push origin main

echo "تمت عملية الرفع بنجاح يا شريكي!"