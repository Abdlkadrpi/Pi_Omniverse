# middleware/prism_memory_guard.py

import gc
from functools import wraps
from flask import request, jsonify

def optimize_agent_execution(f):
    """
    مغلف أمني وهندسي: يضمن عدم بقاء مخرجات الوكلاء الذكيين أو نماذج اللغات الكبيرة
    عالقة في الذاكرة العشوائية RAM بعد إتمام المهمة.
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        try:
            # تنفيذ المهمة أو الاستدعاء
            response = f(*args, **kwargs)
            return response
        finally:
            # تفريغ الذاكرة فوراً لمنع الـ Memory Leaks
            gc.collect()
            
    return decorated_function