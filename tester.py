
import sys
import os

# إضافة المجلد الحالي للمسار
sys.path.append(os.getcwd())

try:
    from core.pi_rc1_token import UnitToken
    from core.ai_oracle import evaluate_content

    token = UnitToken()
    score = evaluate_content('VIDEO')
    
    # تنفيذ وتوليد الأرباح
    result = token.process_reward('User_Alpha', score)
    
    print('\n✅ تم تشغيل المحرك بنجاح!')
except Exception as e:
    print(f'\n❌ حدث خطأ أثناء التشغيل: {e}')

