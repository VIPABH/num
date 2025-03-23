import os
from telethon import TelegramClient, events, Button

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
