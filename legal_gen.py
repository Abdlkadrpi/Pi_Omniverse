import os

html_content = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>OmniVerse Legal & Privacy</title>
    <style>body { font-family: sans-serif; line-height: 1.6; padding: 20px; }</style>
</head>
<body>
    <h1>OmniVerse: Privacy & Terms of Service</h1>
    
    <h2>Arabic (العربية)</h2>
    <p><strong>سياسة الخصوصية:</strong> تلتزم OmniVerse بحماية بياناتك. نحن نستخدم Pi SDK للمصادقة فقط. لا يتم تخزين كلمات المرور أو البيانات الحساسة.</p>
    <p><strong>شروط الاستخدام:</strong> نظام LYO هو اقتصاد تجريبي ذكي. المستخدم مسؤول عن أمان محفظته.</p>
    
    <hr>
    
    <h2>English</h2>
    <p><strong>Privacy Policy:</strong> OmniVerse is committed to user privacy. We use Pi SDK for authentication only. No sensitive user data is stored.</p>
    <p><strong>Terms of Service:</strong> The LYO protocol is an experimental smart economy. Users are responsible for their own wallet security.</p>
</body>
</html>
"""

def create_legal_page():
    # التأكد من وجود مجلد ui
    if not os.path.exists('ui'):
        os.makedirs('ui')
    
    with open('ui/legal.html', 'w', encoding='utf-8') as f:
        f.write(html_content)
    print("[+] Legal page created successfully at ui/legal.html")

if __name__ == "__main__":
    create_legal_page()