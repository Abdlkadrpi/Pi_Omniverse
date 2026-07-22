#!/bin/bash

# 1. إعداد التجاهل التلقائي
echo "node_modules" > .gitignore
echo ".env" >> .gitignore
echo "__pycache__" >> .gitignore

# 2. إزالة المجلدات غير المرغوبة من تتبع git (إذا كانت موجودة)
git rm -r --cached node_modules --ignore-unmatch
git rm -r --cached __pycache__ --ignore-unmatch

# 3. إتمام عملية الرفع التلقائي
git add .
git commit -m "Auto-deploy: Cleanup and infrastructure update"
git push origin main

echo "--- تم الرفع بنجاح! تحقق من منصة Render الآن ---"