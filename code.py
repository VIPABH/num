from telethon.sync import TelegramClient
from telethon.tl.functions.channels import GetParticipantsRequest
from telethon.tl.types import ChannelParticipantsBanned
import os
from datetime import datetime

# جلب بيانات البوت من المتغيرات البيئية
api_id = os.getenv('API_ID')
api_hash = os.getenv('API_HASH')
bot_token = os.getenv('BOT_TOKEN')

# إنشاء العميل الأساسي
client = TelegramClient('bot', api_id, api_hash).start(bot_token=bot_token)

async def get_users_without_write_permission(event):
    group_username = event.chat_id  # الحصول على معرف المجموعة من الحدث

    # جلب المشاركين المحظورين فقط باستخدام العميل الأساسي
    participants = await client(GetParticipantsRequest(
        channel=group_username,
        filter=ChannelParticipantsBanned(q=""),  # استخدم قيمة فارغة بدلاً من None
        offset=0,
        limit=100,  # جلب أول 100 مستخدم محظور
        hash=0
    ))

    # إذا لم يكن هناك مشاركون محظورون
    if not participants.users:
        await event.reply("لا يوجد مستخدمون محظورون في هذه المجموعة.")
        return

    # إرسال النتائج للمستخدم الذي أرسل الأمر
    for user in participants.users:
        # إذا كان للمستخدم اسم مستخدم
        mention = f"[@{user.username}](https://t.me/@{user.username})" if user.username else f"[{user.first_name}](tg://user?id={user.id})"
        
        # نبحث عن وقت الحظر الفعلي من خلال `banned_until`
        banned_user = next((b for b in participants.users if b.id == user.id), None)
        
        if banned_user and hasattr(banned_user, 'banned_until') and banned_user.banned_until:
            ban_time = banned_user.banned_until.strftime("%I:%M:%S %p")  # تنسيق الساعة 12
            ban_date = banned_user.banned_until.strftime("%Y-%m-%d")  # تاريخ الحظر
        else:
            ban_time = "لا يوجد وقت محدد للحظر"
            ban_date = "لا يوجد تاريخ للحظر"

        await event.reply(f"User: {user.id} - {mention}\nBanned Date: {ban_date}\nBanned Time: {ban_time}", parse_mode="md")

# تشغيل الكود عبر حدث
from telethon import events

@client.on(events.NewMessage(pattern='/get_banned'))  # تشغيل الكود عند كتابة الأمر /get_banned
async def handle_event(event):
    await get_users_without_write_permission(event)

# إبقاء البوت قيد التشغيل
client.run_until_disconnected()
