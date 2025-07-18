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
    if not is_assistant(event.chat_id, event.sender_id):
        await chs(event, 'شني خالي كبينه انت مو معاون')
        return
    feature, action = event.pattern_match.groups()
    if feature not in actions:
        return
    lock_key = f"lock:{event.chat_id}:{feature}"    
    if action == "تفعيل":
        r.set(lock_key, "True")
        await chs(event, f'تم تفعيل ال{feature}  تدلل حبيبي')
    else:
        r.set(lock_key, "False")
        await chs(event, f'تم تعطيل ال{feature} تدلل حبيبي')
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
    'format': 'bestaudio',
    'outtmpl': 'downloads/%(title)s.%(ext)s',
    'noplaylist': True,
    'quiet': True,
    'cookiefile': f"{COOKIES_FILE}",
    'postprocessors': [{
        'key': 'FFmpegExtractAudio',
        'preferredcodec': 'mp3',
        'preferredquality': '128',
    }],
}
x = {}
@ABH.on(events.NewMessage(pattern=r'^(يوت|yt|حمل) (.+)'))
async def download_audio(event):
    lock_key = f"lock:{event.chat_id}:يوتيوب"
    z = r.get(lock_key) == "True"
    text = event.raw_text
    parts = text.split(maxsplit=1)
    command = parts[0]
    if not z and command in ['يوت', 'yt']:
        return
    query = event.pattern_match.group(2)
    type = "يوت"
    await botuse(type)
    c = event.chat_id
    try:
        b = Button.url('CHANNEL', 'https://t.me/X04OU')
        for val in audio_cache.values():
            if isinstance(val, dict) and query in val.get("queries", []):
                await ABH.send_file(
                    c,
                    file=val["file_id"],
                    caption="[ENJOY DEAR](https://t.me/VIPABH_BOT)",
                    attributes=[
                        DocumentAttributeAudio(
                            duration=val.get("duration", 0),
                            title=val.get("title"),
                            performer='ANYMOUS'
                        )
                    ],
                    buttons=[b],
                    reply_to=event.message.id
                )
                return
        msg = await event.reply(f'جاري البحث عن {query}')
        x.setdefault(event.chat_id, {}).setdefault(event.sender_id, set()).add(msg.id)
        ydl = YoutubeDL(YDL_OPTIONS)
        search_result = await asyncio.to_thread(ydl.extract_info, f"ytsearch:{query}", download=False)
        if 'entries' not in search_result or not search_result['entries']:    
            await event.reply("لم يتم العثور على نتائج.")
            return
        video_info = search_result['entries'][0]
        video_id = video_info.get('id')
        duration = video_info.get("duration", 0)
        if duration > 2700:
            await chs(event, " لا يمكن تحميل مقاطع أطول من 45 دقيقة.")
            return
        if video_id in audio_cache:
            val = audio_cache[video_id]
            if "queries" not in val:
                val["queries"] = []
            if query not in val["queries"]:
                val["queries"].append(query)
                save_cache()
            await ABH.send_file(
                c,
                file=val["file_id"],
                caption="[ENJOY DEAR](https://t.me/VIPABH_BOT)",
                attributes=[
                    DocumentAttributeAudio(
                        duration=val.get("duration", 0),
                        title=val.get("title"),
                        performer='ANYMOUS'
                    )
                ],
                buttons=[b],
                reply_to=event.message.id
            )
            return
        msg_ids = x.get(event.chat_id, {}).get(event.sender_id)
        if msg_ids:
            for m_id in msg_ids:
                try:
                    await event.client.edit_message(event.chat_id, m_id, f'جاري تنزيل {query}')
                except Exception as e:
                    await hint(f"خطأ في تحديث الرسالة: {str(e)}")
                    pass
        else:
            await event.reply(f'جاري تنزيل {query}')
        download_info = await asyncio.to_thread(ydl.extract_info, f"ytsearch:{query}", download=True)
        downloaded_video = download_info['entries'][0]
        file_path = ydl.prepare_filename(downloaded_video).replace(".webm", ".mp3").replace(".m4a", ".mp3")
        msg = await ABH.send_file(
            c,
            file=file_path,
            caption="[ENJOY DEAR](https://t.me/VIPABH_BOT)",
            attributes=[
                DocumentAttributeAudio(
                    duration=downloaded_video.get("duration", 0),
                    title=downloaded_video.get("title"),
                    performer='ANYMOUS'
                )
            ],
            buttons=[b],
            reply_to=event.message.id
        )
        audio_cache[downloaded_video.get("id")] = {
            "file_id": msg.file.id,
            "title": downloaded_video.get("title"),
            "duration": downloaded_video.get("duration", 0),
            "queries": [query]
        }
        save_cache()
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
@ABH.on(events.NewMessage(pattern=r'^ارسل الملفات$', from_users=[1910015590]))
async def send_all_files(event):
    try:
        folder_path = "."
        files = [f for f in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path, f))]
        if not files:
            await event.reply("❗️لا توجد ملفات متاحة للإرسال في المجلد.")
            return
        await event.reply(f"📤 جارٍ إرسال {len(files)} ملفًا، يرجى الانتظار...")
        for file_name in files:
            file_path = os.path.join(folder_path, file_name)
            await ABH.send_file(event.chat_id, file=file_path)
        await event.reply("✅ تم إرسال جميع الملفات بنجاح.")
    except Exception as e:
        await event.reply(f"حدث خطأ أثناء إرسال الملفات: {e}")
@ABH.on(events.NewMessage(pattern=r'^ارسل ملف (.+)$', from_users=[1910015590]))
async def send_file(event):
    type = "ارسال ملف"
    await botuse(type)
    file_name = event.pattern_match.group(1)
    if not os.path.exists(file_name):
        return await event.reply("❗️الملف غير موجود.")
    await event.reply("📤 جاري ارسال الملف...")
    await ABH.send_file(event.chat_id, file=file_name)
@ABH.on(events.NewMessage(pattern=r'^حذف ملف (.+)$', from_users=[1910015590]))
async def delete_file(event):
    type = "حذف ملف"
    await botuse(type)
    file_name = event.pattern_match.group(1)
    if not os.path.exists(file_name):
        return await event.reply("الملف غير موجود.")
    os.remove(file_name)
    await event.reply("✅ تم حذف الملف بنجاح.")
@ABH.on(events.NewMessage(pattern=r'^الملفات$', from_users=[1910015590]))
async def list_files(event):
    type = "قائمة الملفات"
    await botuse(type)
    files = os.listdir('.')
    if not files:
        return await event.reply("❗️لا توجد ملفات في المجلد الحالي.")
    file_list = "\n" .join(files)
    await event.reply(f"📂 قائمة الملفات\n{file_list}")
