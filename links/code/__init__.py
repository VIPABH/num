import os
from telethon import TelegramClient, events, Button
from code.module1 import some_function
from code.module2 import another_function

# ✅ التحقق من وجود المتغيرات البيئية
api_id = os.getenv('API_ID')
api_hash = os.getenv('API_HASH')
bot_token = os.getenv('BOT_TOKEN')

if not api_id or not api_hash or not bot_token:
    raise ValueError("One or more required environment variables are missing.")

# ✅ إنشاء عميل التليجرام
ABH = TelegramClient('code', api_id, api_hash).start(bot_token=bot_token)
print("Bot started successfully!")

# ✅ الوظائف الرئيسية
def main():
    print("This is the main program!")
    some_function()
    another_function()  # تشغيل الوظيفة من module2.py

if __name__ == "__main__":
    main()
    print("Starting Telegram bot...")
    ABH.run_until_disconnected()  # ✅ تشغيل البوت مرة واحدة فقط
