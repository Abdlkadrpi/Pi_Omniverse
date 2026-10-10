import sys
sys.path.append('Omniverse')
import telebot
from Omniverse_Auto_Agent import bot
print('🚀 [خوادم التلغرام] تم تفعيل السحب السيادي المباشر...')
bot.infinity_polling(timeout=20, long_polling_timeout=10)
