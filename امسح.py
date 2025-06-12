from other import botuse, is_assistant
from telethon.tl.types import (
    MessageMediaDocument,
    DocumentAttributeAudio)
from telethon import events
from Resources import chs
from ABH import ABH
import os, json
FILE_PATH = "media_messages.json"
if os.path.exists(FILE_PATH):
    with open(FILE_PATH, "r", encoding="utf-8") as f:
        media_messages = json.load(f)
else:
    media_messages = {}
def save_media_messages():
    with open(FILE_PATH, "w", encoding="utf-8") as f:
        json.dump(media_messages, f, ensure_ascii=False, indent=2)
@ABH.on(events.NewMessage)
async def store_media_messages(event):
    chat_id = str(event.chat_id)
    msg = event.message
    if msg.media:
        if isinstance(msg.media, MessageMediaDocument):
            if any(isinstance(attr, DocumentAttributeAudio) for attr in msg.media.document.attributes):
                return
        if chat_id not in media_messages:
            media_messages[chat_id] = []
        if msg.id not in media_messages[chat_id]:
            media_messages[chat_id].append(msg.id)
            save_media_messages()
@ABH.on(events.NewMessage(pattern='^امسح|تنظيف$'))
async def delete_stored_media(event):
    type = "امسح"
    await botuse(type)
    if not is_assistant(event.chat_id, event.sender_id):
        await event.reply('شني خالي كبينه انت مو معاون')
        return
    chat_id = str(event.chat_id)
    deleted_count = 0
    if chat_id in media_messages and media_messages[chat_id]:
        for msg_id in media_messages[chat_id]:
            await ABH.delete_messages(int(chat_id), msg_id)
            deleted_count += 1
        media_messages[chat_id] = []
        save_media_messages()
        await event.reply(f'تم حذف {deleted_count} ب نجاح 🗑️🗑️')
@ABH.on(events.NewMessage(pattern='^عدد|كشف ميديا|كشف الميديا$'))
async def count_media_messages(event):
    type = "كشف ميديا"
    await botuse(type)
    chat_id = str(event.chat_id)
    if chat_id in media_messages and media_messages[chat_id]:
        count = len(media_messages[chat_id])
        await chs(event, f'عدد الرسائل الموجهه للحذف {count} 👍🏾')        
    else:
        await event.reply("المجموعة ما بيها ميديا مخزنه للحذف")
@ABH.on(events.NewMessage(pattern='^ثبتها| تخطي المسح|الغاء مسح$'))
async def undel(event):
    type = "تخطي المسح"
    await botuse(type)
    if not is_assistant(event.chat_id, event.sender_id):
        await event.reply('شني خالي كبينه انت مو معاون')
        return
    r = await event.get_reply_message()
    if not r:
        await chs(event, 'يجب الرد على رسالة وسائط.')
        return
    if not r.media:
        await chs(event, 'يا لوتي لازم ترد على رساله بيها ميديا')
        return
    chat_id = str(event.chat_id)
    msg_id = r.id
    if chat_id in media_messages and msg_id in media_messages[chat_id]:
        media_messages[chat_id].remove(msg_id)
        save_media_messages()
        await chs(event,"👌 تم استثناء هذه الرسالة من الحذف.")
    else:
        await chs(event, "الرسالة هاي بالاصل ما مسجلة ```ما تنحذف يمي```")
@ABH.on(events.NewMessage(pattern='^تفريغ$'))
async def delalmedia_message(event):
    type = "تفريغ"
    await botuse(type)
    if not is_assistant(event.chat_id, event.sender_id):
        await event.reply('شني خالي كبينه انت مو معاون')
        return
    chat_id = event.chat_id
    media_messages[chat_id].clear()
    await chs(event, 'تم مسح قائمة التنظيف👍🏾👍🏾')
