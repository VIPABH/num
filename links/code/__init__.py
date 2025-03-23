import os
from telethon import TelegramClient
# from code.module1 import some_function
# from code.module2 import another_function

# ✅ إعداد متغيرات البيئة
api_id = os.getenv('API_ID')
api_hash = os.getenv('API_HASH')
bot_token = os.getenv('BOT_TOKEN')

if not api_id or not api_hash or not bot_token:
    raise ValueError("One or more required environment variables are missing.")

# ✅ إنشاء كائن البوت
ABH = TelegramClient('code', api_id, api_hash).start(bot_token=bot_token)
# print("Bot started successfully!")

# # ✅ تشغيل الوظائف من الملفات الأخرى
# def main():
#     print("This is the main program!")
#     some_function()         # تشغيل دالة من module1
#     another_function()      # تشغيل دالة من module2

# if __name__ == "__main__":
#     main()
#     print("Starting Telegram bot...")
    ABH.run_until_disconnected()  # تشغيل البوت فقط في `main.py`
