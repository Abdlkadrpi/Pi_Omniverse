#!/bin/bash

# 1. تحديد مسار ملف الجافا سكريبت (تأكد من الاسم الصحيح للملف عندك)
JS_FILE="ui/script.js"

# 2. إضافة كود المصادقة التلقائي في بداية الملف
echo "جاري تحديث كود المصادقة في $JS_FILE..."
sed -i '1i // Pi Network Auth Init\nconst Pi = window.Pi;\nPi.init({ version: "2.0" });\n\nasync function authenticateUser() {\n    try {\n        const user = await Pi.authenticate(["username", "payments", "wallet_address"], (payment) => {});\n        console.log("Welcome Commander: " + user.user.username);\n    } catch (err) {\n        console.error(err);\n    }\n}\n\nauthenticateUser();\n' $JS_FILE

# 3. أوامر الرفع التلقائي إلى GitHub
echo "جاري الرفع إلى GitHub..."
git add .
git commit -m "تفعيل نظام المصادقة التلقائي لمدينة أومني فيرس الذكية"
git push origin main

echo "✅ تم التحديث والرفع بنجاح! يمكنك الآن تجربة التطبيق في متصفح باي."
