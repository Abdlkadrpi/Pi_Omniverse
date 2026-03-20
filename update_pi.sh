#!/bin/bash
HTML_FILE="ui/index.html"
echo "جاري تجهيز بوابة الدخول لمدينتك الذكية..."
sed -i '/<head>/a \    <script src="https://sdk.minepi.com/pi-sdk.js"></script>\n    <script>\n      const Pi = window.Pi;\n      Pi.init({ version: "2.0" });\n      async function authenticateUser() {\n        try {\n          const user = await Pi.authenticate(["username", "payments", "wallet_address"], (payment) => {});\n          console.log("Welcome Commander: " + user.user.username);\n        } catch (err) {\n          console.error(err);\n        }\n      }\n      window.onload = authenticateUser;\n    </script>' $HTML_FILE
git add .
git commit -m "تفعيل نظام المصادقة النهائي"
git push origin main
echo "✅ تم التحديث والرفع بنجاح!"
