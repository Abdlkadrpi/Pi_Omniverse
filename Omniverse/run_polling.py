import sys
import os
import time
import requests
sys.path.append(os.getcwd())

session = requests.Session()
adapter = requests.adapters.HTTPAdapter(max_retries=5)
session.mount('https://', adapter)

import telebot
from telebot import apihelper

def smart_request_sender(method, url, **kwargs):
    if 'timeout' not in kwargs or kwargs['timeout'] is None:
        kwargs['timeout'] = 60
    return session.request(method, url, **kwargs)

apihelper.CUSTOM_REQUEST_SENDER = smart_request_sender

from Omniverse_Auto_Agent import bot

print('[OMNIVERSE] Clearing old webhooks from Telegram servers...')
try:
    bot.remove_webhook()
    print('[SUCCESS] Webhook removed successfully!')
except Exception as e:
    print(f'[WARNING] Webhook removal skipped: {e}')

print('[SYSTEM] Sovereign Core is now listening for messages...')

while True:
    try:
        bot.infinity_polling(timeout=60, long_polling_timeout=30)
    except Exception as e:
        print(f'[RETRY] Reconnecting in 5 seconds due to: {e}')
        time.sleep(5)
