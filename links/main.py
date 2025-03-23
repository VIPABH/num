from code import ABH, reply  # ✅ استيراد ABH و الوظائف المطلوبة

print("✅ Running main.py...")

def main():
    print("✅ This is the main program!")
    reply()         

if __name__ == "__main__":
    main()
    print("✅ Starting Telegram bot...")
    ABH.run_until_disconnected()
