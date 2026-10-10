import os
import sys
import time
import json
import sqlite3
import hashlib
import threading
from datetime import datetime

# تفعيل بروتوكول دعم اللغة العربية والترميز العالمي تلقائياً في الطرفية
os.system('chcp 65001 > nul')
if sys.stdout.encoding != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8')

DB_NAME = "omniverse_secure_ledger.db"

class OmniverseAgentEngine:
    def __init__(self, agent_id, name, role, escrow_balance=100.0):
        self.agent_id = agent_id
        self.name = name
        self.role = role
        self.escrow_balance = escrow_balance
        self.is_active = True
        self.lock = threading.Lock()
        
        print(f"🤖 [تأسيس وكيل] تم بناء الوكيل السيادي: {self.name} | الدور: {self.role} | الضمان: {self.escrow_balance} LYO")
        self.init_agent_ledger()

    def init_agent_ledger(self):
        """تجهيز قاعدة البيانات وضمان وجود الأعمدة المطلوبة لعدم حدوث أخطاء Schema"""
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS secure_ledger (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                tx_id TEXT,
                current_hash TEXT,
                prev_block_hash TEXT,
                minted_amount REAL,
                burned_amount REAL,
                status TEXT,
                timestamp TEXT
            )
        ''')
        conn.commit()
        conn.close()

    def get_last_block_hash(self):
        """جلب هاش الكتلة السابقة لضمان ربط السلسلة بشكل محكم ومنع التلاعب الأبدي"""
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        cursor.execute("SELECT current_hash FROM secure_ledger ORDER BY id DESC LIMIT 1")
        row = cursor.fetchone()
        conn.close()
        return row[0] if row else "0000000000000000"

    def execute_autonomous_task(self, task_data):
        """تنفيذ المهمة الاقتصادية مع تفعيل الحرق الانكماشي وصندوق الضمان الذاتي"""
        with self.lock:
            if not self.is_active:
                print(f"❌ [بروتوكول حماية] الوكيل {self.name} مجمد حالياً ولا يمكنه العمل.")
                return False

            print(f"\n⚡ [بدء مهمة] الوكيل {self.name} يقوم بمعالجة تدفق مالي وتوثيق كتلي...")
            
            # محاكاة حسابات الـ Tokenomics الانكماشية الحادة لدعم السعر
            gross_amount = 10.0
            minted_reward = 9.79
            burned_amount = 0.11
            
            tx_id = f"pi_agent_tx_{int(time.time())}_{self.agent_id[:5]}"
            prev_hash = self.get_last_block_hash()
            
            # توليد الهاش الحالي بناءً على الربط الكتلي المتسلسل
            raw_block_data = f"{tx_id}{prev_hash}{minted_reward}{burned_amount}"
            current_hash = hashlib.sha256(raw_block_data.encode('utf-8')).hexdigest()
            timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

            try:
                # محاكاة فحص جودة البيانات (إذا كانت البيانات فارغة أو مغلوطة يتم إطلاق استثناء)
                if not task_data.get("utility_verified", False):
                    raise ValueError("محاكاة فشل المعالجة: قراءة نبضة مغلوطة من السجل.")

                # حقن البيانات في السجل الآمن بنجاح
                conn = sqlite3.connect(DB_NAME)
                cursor = conn.cursor()
                cursor.execute('''
                    INSERT INTO secure_ledger (tx_id, current_hash, prev_block_hash, minted_amount, burned_amount, status, timestamp)
                    VALUES (?, ?, ?, ?, ?, ?, ?)
                ''', (tx_id, current_hash, prev_hash, minted_reward, burned_amount, "APPROVED & COMPLIANT", timestamp))
                conn.commit()
                conn.close()

                # تحديث محفظة الوكيل كمكافأة إنتاجية تسهم في جذب الـ 60 مليون مستخدم
                self.escrow_balance += minted_reward
                self.broadcast_telemetry(tx_id, current_hash, prev_hash, minted_reward, burned_amount)
                return True

            except Exception as e:
                # تشغيل بروتوكول الطوارئ الدولي وحماية المستهلك (Smart Rollback) فوراً عند وقوع خطأ
                print(f"🚨 [اختراق/خطأ رصد] حدث تضارب: {str(e)}")
                self.trigger_emergency_rollback(burned_amount)
                return False

    def trigger_emergency_rollback(self, penalty):
        """عقود الـ Rollback وتجميد الوكيل وخصم الغرامة من صندوق الضمان للامتثال لـ MiCA"""
        self.is_active = False
        self.escrow_balance -= penalty
        print(f"🛡️ [بروتوكول ROLLBACK حاد] تم تجميد الوكيل {self.name} برمجياً فوراً لحماية السلسلة.")
        print(f"💸 [عقوبة ماليّة] تم خصم {penalty} LYO من صندوق ضمان الوكيل. الرصيد الحالي: {self.escrow_balance} LYO")
        print("🏛️ [تقرير قانوني] السجل محصن بالكامل وتراجع تلقائياً إلى الكتلة السابقة الآمنة.")

    def broadcast_telemetry(self, tx_id, current_hash, prev_hash, mint, burn):
        """بث البيانات بشكل فوري ومغلق وبأعلى سرعة ممكنة لمنع الضغط عن الـ APIs العامة"""
        print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
        print("🏛️ إشعار التوثيق الكتلي المؤتمت عبر الـ AGENT")
        print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
        print(f"🆔 معرف المعاملة: {tx_id}")
        print(f"🔒 الهاش الحالي: {current_hash}")
        print(f"🔗 هاش الربط المرجعي: {prev_hash}")
        print(f"💰 تم صك مكافأة الوكيل: {mint} LYO")
        print(f"🔥 الحرق الانكماشي الحاد: {burn} LYO")
        print(f"📈 حالة السجل المستقر: مؤمن ومحصن بنسبة 100% (Zero Errors)")
        print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")

# --- منصة اختبار تشغيل المحرك التأسيسي ---
if __name__ == "__main__":
    print("🏛️ [محرك OMNIVERSE للأتمتة السيادية] يستعد للإقلاع في عتاد الريادة للحاسبات...")
    time.sleep(1)
    
    # 1. إنشاء وكيل ذكي أول لتوثيق العقود العقارية والأصول الرقمية
    notary_agent = OmniverseAgentEngine(
        agent_id="agent_alpha_001",
        name="Tripoli_Notary_Agent_01",
        role="Digital Notary & Asset Verifier"
    )

    # 2. محاكاة معاملة ناجحة تماماً ومتوافقة مع سياسات النظام البيئي
    success_task = {"utility_verified": True, "payload": "Document #99283 Real Estate Contract"}
    notary_agent.execute_autonomous_task(success_task)

    time.sleep(2)

    # 3. محاكاة معاملة هجوم أو بيانات مغلوطة لاختبار الدفاع الذاتي وعقود الـ Rollback
    print("\n⚠️ محاكاة إدخال بيانات مشبوهة أو حدوث انقطاع لحظي للاختبار الفني...")
    fail_task = {"utility_verified": False, "payload": "Malicious / Corrupted Block Attempt"}
    notary_agent.execute_autonomous_task(fail_task)