from code import ABH, some_function, another_function  # ✅ استيراد ABH و الوظائف المطلوبة

print("✅ Running main.py...")

def main():
    print("✅ This is the main program!")
    reply()         
    reply_abh()      

if __name__ == "__main__":
    main()
    print("✅ Starting Telegram bot...")
    ABH.run_until_disconnected()
