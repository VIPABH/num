import os
from telethon import TelegramClient

# تحميل المتغيرات
api_id = os.getenv('API_ID')
api_hash = os.getenv('API_HASH')
bot_token = os.getenv('BOT_TOKEN')

if not api_id or not api_hash or not bot_token:
    raise ValueError("One or more required environment variables are missing.")

# إنشاء كائن البوت ليكون متاحًا للاستيراد
ABH = TelegramClient('code', api_id, api_hash).start(bot_token=bot_token)

# استيراد الدوال لجعلها متاحة عند استيراد `code`
from .module1 import reply
