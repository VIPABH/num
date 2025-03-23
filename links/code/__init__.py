import os
from telethon import TelegramClient, events, Button
api_id = os.getenv('API_ID')      
api_hash = os.getenv('API_HASH')  
bot_token = os.getenv('BOT_TOKEN')
ABH = TelegramClient('code', api_id, api_hash).start(bot_token=bot_token)
print("its worke")
ABH.run_until_disconnected()
