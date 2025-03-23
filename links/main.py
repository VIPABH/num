import os
from code import ABH, some_function
from telethon import events
import asyncio

print("✅ Running main.py...")

# دالة رئيسية مخصصة للمهام غير المتزامنة
async def main():
    print("✅ This is the main program!")

    # تشغيل الوظائف المتزامنة
    reply()
    reply_abh()

    # التأكد من أن البوت يعمل
    print("✅ Starting Telegram bot...")

    # تشغيل البوت وانتظار الأحداث
    await ABH.run_until_disconnected()

if __name__ == "__main__":
    # استخدام asyncio لتشغيل الوظيفة الرئيسية
    asyncio.run(main())
