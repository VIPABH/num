# main.py
from code.module1 import some_function
from code.module2 import function2
from code.__init__ import ABH  # استيراد ABH من links/__init__.py
from telethon import TelegramClient
import os
api_id = os.getenv('API_ID')      
api_hash = os.getenv('API_HASH')  
bot_token = os.getenv('BOT_TOKEN')
ABH = TelegramClient('code', api_id, api_hash).start(bot_token=bot_token)
print('its run')
def main():
    print("This is the main program!")
    some_function()
    function2()
if __name__ == "__main__":
    main()
ABH.run_until_disconnected()
