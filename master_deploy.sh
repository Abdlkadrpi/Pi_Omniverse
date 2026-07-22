#!/bin/bash

echo "--- بدء عملية التحديث الشاملة ---"

# 1. تنظيف البيئة من الملفات المؤقتة
rm -rf __pycache__
echo "node_modules" > .gitignore
echo "assets.db-journal" >> .gitignore

# 2. تنظيف قاعدة البيانات (تصفير المعلقات)
echo "--- تنظيف قاعدة البيانات من العمليات المعلقة ---"
sqlite3 assets.db "DELETE FROM assets WHERE payment_tx IS NULL OR payment_tx = '';"

# 3. إتمام عملية الرفع
git add .
git commit -m "Auto-Deploy: Infrastructure Cleanup & Database Sync"
git push origin main

echo "--- تم الرفع بنجاح! السيرفر يقوم الآن بإعادة البناء (Deploying...) ---"