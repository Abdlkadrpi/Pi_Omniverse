class UnitToken:
    def process_reward(self, user, score):
        tax = (score * 0.1) * 0.05
        print(f'\n--- 💰 سجل الأرباح ---')
        print(f'المستخدم: {user} | حصة القائد: {tax:.4f} $UNIT')

