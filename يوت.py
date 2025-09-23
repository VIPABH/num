from telethon.tl.types import DocumentAttributeAudio
from other import botuse, is_assistant
from telethon import events, Button
from yt_dlp import YoutubeDL
from Program import r, chs
from Resources import hint
import os, asyncio, json
from ABH import ABH
actions = ['يوتيوب', 'تقييد', 'ردود', 'تنظيف']
@ABH.on(events.NewMessage(pattern=r'^ال(\w+)\s+(تفعيل|تعطيل)$'))
async def toggle_feature(event):
    if not event.is_group:
        return
    if not is_assistant(event.chat_id, event.sender_id):
        await chs(event, 'شني خالي كبينه انت مو معاون')
        return
    feature, action = event.pattern_match.groups()
    if feature not in actions:
        return
    lock_key = f"lock:{event.chat_id}:{feature}"
    current_status = r.get(lock_key)
    if action == "تفعيل":
        if current_status == "True":
            await chs(event, f'الميزة {feature} مفعلة مسبقاً ✅')
        else:
            r.set(lock_key, "True")
            await chs(event, f'تم تفعيل {feature} بنجاح ✅')
    else:
        if current_status == "False":
            await chs(event, f'الميزة {feature} معطلة مسبقاً ❌')
        else:
            r.set(lock_key, "False")
            await chs(event, f'تم تعطيل {feature} بنجاح ❌')
COOKIES_FILE = 'c.txt'
if not os.path.exists("downloads"):
    os.makedirs("downloads")
CACHE_FILE = "audio_cache.json"
if os.path.exists(CACHE_FILE):
    with open(CACHE_FILE, "r", encoding="utf-8") as f:
        audio_cache = json.load(f)
else:
    audio_cache = {}
def save_cache():
    with open(CACHE_FILE, "w", encoding="utf-8") as f:
        json.dump(audio_cache, f, ensure_ascii=False, indent=2)
YDL_OPTIONS = {
    'format': 'worstaudio',
    'outtmpl': 'downloads/%(title)s.%(ext)s',
    'noplaylist': True,
    'quiet': True,
    'cookiefile': f"{COOKIES_FILE}",
}
x = {}
@ABH.on(events.NewMessage(pattern=r'^(يوت|yt|حمل) (.+)'))
async def download_audio(event):
    if not event.is_group and event.text != 'حمل':
        return
    ydl = YoutubeDL(YDL_OPTIONS)
    lock_key = f"lock:{event.chat_id}:يوتيوب"
    if not r.get(lock_key) == "True" and event.text != 'حمل':
        return
    query = event.pattern_match.group(2)
    c = event.chat_id
    b = Button.url('CHANNEL', 'https://t.me/X04OU')
    try:
        msg = await event.reply("⏳ جاري المعالجة ...")
        x[event.id] = msg
        if query.startswith("http://") or query.startswith("https://"):
            video_url = query
        else:
            search_result = await asyncio.to_thread(
                ydl.extract_info, f"ytsearch:{query}", download=False
            )
            if not search_result.get('entries'):
                await msg.edit("❌ لم يتم العثور على نتائج.")
                return
            video_info = search_result['entries'][0]
            video_url = f"https://www.youtube.com/watch?v={video_info['id']}"
        info = await asyncio.to_thread(
            ydl.extract_info, video_url, download=False
        )
        video_id = info['id']
        duration = info.get("duration", 0)
        title = info.get("title")
        if duration > 2700:
            await msg.edit("⏰ لا يمكن تحميل مقاطع أطول من 45 دقيقة.")
            return
        if video_id in audio_cache:
            val = audio_cache[video_id]
            await ABH.send_file(
                c,
                file=val["file_id"],
                caption="[ENJOY DEAR](https://t.me/VIPABH_BOT)",
                attributes=[DocumentAttributeAudio(
                    duration=val.get("duration", 0),
                    title=val.get("title"),
                    performer='ANYMOUS'
                )],
                buttons=[b],
                reply_to=event.message.id
            )
            await msg.delete()
            return
        await msg.edit(f'⬇️ جاري تنزيل: {title}')
        download_info = await asyncio.to_thread(
            ydl.extract_info, video_url, download=True
        )
        file_path = ydl.prepare_filename(download_info)
        sent = await ABH.send_file(
            c,
            file=file_path,
            caption="[ENJOY DEAR](https://t.me/VIPABH_BOT)",
            attributes=[DocumentAttributeAudio(
                duration=download_info.get("duration", 0),
                title=download_info.get("title"),
                performer='ANYMOUS'
            )],
            buttons=[b],
            reply_to=event.message.id
        )
        audio_cache[video_id] = {
            "file_id": sent.file.id,
            "title": title,
            "duration": duration,
            "queries": [query]
        }
        save_cache()
        await msg.delete()
    except Exception as e:
        await ABH.send_message(1910015590, f"Error: {str(e)}")
@ABH.on(events.NewMessage(pattern='^اضف كوكيز$', from_users=[1910015590]))
async def add_cookie(event):
    type = "كوكيز"
    await botuse(type)
    r = await event.get_reply_message()
    if not r or not r.document:
        return await event.reply("❗️يرجى الرد على رسالة تحتوي على ملف كوكيز.")    
    tmp_file = "temp_cookie.txt"
    await r.download_media(file=tmp_file)
    with open(tmp_file, "r", encoding="utf-8") as f:
        content = f.read()
    os.remove(tmp_file)
    if os.path.exists("cookie.json"):
        os.remove("cookie.json")
    with open("cookie.json", "w", encoding="utf-8") as f:
        json.dump({"cookie_data": content}, f, ensure_ascii=False, indent=2)
    await event.reply(" تم حفظ الكوكيز داخل ملف JSON بنجاح.")
