import os
from telethon import TelegramClient, events, Button
from .. import *
try:
    api_id = os.getenv('API_ID')
    api_hash = os.getenv('API_HASH')
    bot_token = os.getenv('BOT_TOKEN')

    if not api_id or not api_hash or not bot_token:
        raise ValueError("One or more required environment variables are missing.")

    ABH = TelegramClient('code', api_id, api_hash).start(bot_token=bot_token)
    print("Bot started successfully!")
    ABH.run_until_disconnected()

except Exception as e:
    print(f"An error occurred: {e}")
    from code.module1 import some_function
from code.module2 import function2
print("Running main.py...")
some_function()
another_function()  # تشغيل الوظيفة من module2.py
def main():
    print("This is the main program!")
    some_function()
    function2()
if __name__ == "__main__":
    main()

# تشغيل البوت
print("Starting Telegram bot...")
ABH.run_until_disconnected()

