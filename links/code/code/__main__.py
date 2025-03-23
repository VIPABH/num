import asyncio
from .code import code
from .code import code8

# دالة main غير المتزامنة
async def main():
    print("This is the main entry point of the 'links' package")
    await code()  # استدعاء دالة code بشكل غير متزامن
    await code8()  # استدعاء دالة code8 بشكل غير متزامن
    await l313l.connect()  # استدعاء connect بشكل غير متزامن

# دالة لبدء تحميل الإضافات بشكل غير متزامن
async def startup_process():
    await load_plugins("code")
    await load_plugins("code8")

# تشغيل دالة main باستخدام asyncio.run
if __name__ == '__main__':
    asyncio.run(main())  # استخدام asyncio.run لتشغيل الدالة main
