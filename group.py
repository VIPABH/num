from telethon.tl.functions.channels import GetParticipantRequest
from db import save_date, get_saved_date #type: ignore
from ABH import ABH, events #type: ignore
from datetime import datetime, timedelta
import asyncio, os, json, time, random, re
from hijri_converter import Gregorian
from googletrans import Translator
from num2words import num2words
from telethon import Button
from other import botuse
from Resources import *
from Program import chs
from top import *
from telethon.tl.types import (
    MessageExtendedMediaPreview, DocumentAttributeAudio, DocumentAttributeSticker,
    Message, MessageMediaPhoto, MessageMediaDocument, MessageMediaGeo,
    DocumentAttributeVideo, DocumentAttributeAnimated,
    MessageMediaPoll, MessageExtendedMedia,
)
@ABH.on(events.NewMessage(pattern=r"^(رتبتي|رتبت(ه|ة))$"))
async def myrank(e):
    reply_msg=await e.get_reply_message()
    if not reply_msg and e.text=="رتبتي":
        rank=await auth(e)
        if not rank:rank="عضو فقير"
        await chs(e,f"🏷️ رتبتك: ( {rank} )")
        return
    if reply_msg:
        rank=await auth(e,True)
        if not rank:rank="عضو فقير"
        await chs(e,f"🏷️ رتبته: ( {rank} )")
        return
    await chs(e,"⚠️ يرجى استخدام الأمر بشكل صحيح.")
@ABH.on(events.NewMessage(pattern=r'^مخفي اختار'))
async def hidden_choice_handler(event):
    message = event.raw_text
    await botuse("مخفي اختار")
    content = re.sub(r'^مخفي اختار\s*', '', message).strip()
    if not content:
        await event.reply("⚠️ يرجى كتابة جملتين مفصولتين بكلمة (لو) أو (او).")
        return
    match = re.search(r'(.+?)\s+(?:لو|او|أو)\s+(.+)', content)
    if not match:
        await event.reply("⚠️ لم أستطع العثور على المفتاح (لو) أو (او) في الجملة.")
        return
    option1 = match.group(1).strip()
    option2 = match.group(2).strip()
    selected = random.choice([option1, option2])
    await chs(
        event,
        f"🎯 اختاريت: ( {selected} )"
    )
def get_message_type(msg: Message) -> str:
    if msg is None:
        return
    if msg.message and not msg.media:
        return "الرسائل"
    if isinstance(msg.media, MessageExtendedMediaPreview) or isinstance(msg.media, MessageExtendedMedia):
        inner = msg.media.media
        return get_message_type(Message(id=msg.id, media=inner))
    if isinstance(msg.media, MessageMediaPhoto):
        return "الصور"
    if isinstance(msg.media, MessageMediaDocument):
        for attr in msg.media.document.attributes:
            if isinstance(attr, DocumentAttributeAnimated):
                return "المتحركات"
        for attr in msg.media.document.attributes:
            if isinstance(attr, DocumentAttributeVideo):
                if getattr(attr, "round_message", False):
                    return "الفويس نوت"
                return "الفيديوهات"
        for attr in msg.media.document.attributes:
            if isinstance(attr, DocumentAttributeSticker):
                return "الستيكرات"
            if isinstance(attr, DocumentAttributeAudio):
                return "الفويسات" if getattr(attr, "voice", False) else "الصوتيات"
        mime = msg.media.document.mime_type or ""
        if mime.startswith("image/"):
            return "الصور"
        elif mime.startswith("video/"):
            return "الفيديوهات"
        elif mime.startswith("audio/"):
            return "الصوتيات"
        return "الملفات"
    if isinstance(msg.media, MessageMediaGeo):
        return "المواقع"
    if isinstance(msg.media, MessageMediaPoll):
        return "الاستفتاءات"
    return
USER_DATA_FILE = "thift.json"
def load_user_data():
    if os.path.exists(USER_DATA_FILE):
        try:
            with open(USER_DATA_FILE, "r", encoding="utf-8") as file:
                return json.load(file)
        except json.JSONDecodeError:
            return {}
    return {}
def save_user_data(data):
    with open(USER_DATA_FILE, "w", encoding="utf-8") as file:
        json.dump(data, file, ensure_ascii=False, indent=4)
@ABH.on(events.NewMessage(pattern=r'^(?:سرقة|سرقه|خمط)$'))
async def theft(e):
    if not e.is_group:
        return
    user_id = str(e.sender_id)
    user_data = load_user_data()
    user_data.setdefault('سرقة', {})
    user_data.setdefault('مسروق', {})
    current_time = int(time.time())
    cooldown = 10 * 60
    last_play_time = user_data['سرقة'].get(user_id, {}).get('last_play_time', 0)
    last_stolen_time = user_data['مسروق'].get(user_id, {}).get('last_play_time', 0)
    if current_time - last_stolen_time < cooldown:
        remaining = cooldown - (current_time - last_stolen_time)
        minutes, seconds = divmod(remaining, 60)
        await e.reply(f"🪙 تمت سرقتك مؤخرًا! يجب أن تنتظر {minutes:02}:{seconds:02} قبل أن تسرق أحدًا.")
        await react(e, '😞')
        return
    if current_time - last_play_time < cooldown:
        remaining = cooldown - (current_time - last_play_time)
        minutes, seconds = divmod(remaining, 60)
        await e.reply(f"⏳ يجب أن تنتظر {minutes:02}:{seconds:02} قبل أن تسرق مجددًا.")
        await react(e, '😐')
        return
    r = await e.get_reply_message()
    if not r:
        await react(e, '🤔')
        await e.reply('يجب أن ترد على رسالة الشخص الذي تريد سرقته.')
        return
    target_id = str(r.sender_id)
    target = await r.get_sender()
    if target.bot:
        await e.reply('❌ لا يمكنك السرقة من بوت.')
        return
    if target_id == user_id:
        await e.reply('❌ لا يمكنك سرقة نفسك.')
        return
    rank = await auth(e, True)
    if rank and rank != "المعاون":
        await chs(e, f"عذرًا، لا يمكنك السرقة من {rank}.")
        return
    فلوس = points.get(target_id, points.get(str(target_id), 0))
    if فلوس < 10000:
        await chs(e, f'عذرًا، {await ment(target)} فلوسه قليلة جدًا للسرقة 💸')
        return
    stolen_amount = فلوس // 10
    delpoints(target_id, e.chat_id, points, stolen_amount)
    add_points(e.sender_id, e.chat_id, points, stolen_amount)
    await chs(e, f'💰 تمت سرقة {stolen_amount} من {await ment(target)} بنجاح 🎉')
    await react(e, '🎉')
    user_data['سرقة'][user_id] = {'last_play_time': current_time}
    user_data['مسروق'][target_id] = {'last_play_time': current_time}
    save_user_data(user_data)
@ABH.on(events.NewMessage(pattern=r'^تداول$'))
async def trade(event):
    if not event.is_group:
        return
    type = "تداول"
    await botuse(type)
    user_id = str(event.sender_id)
    gid = str(event.chat_id)
    user_data = load_user_data()
    user_data.setdefault('تداول', {})
    user_data['تداول'].setdefault(user_id, {})
    last_play_time = user_data['تداول'][user_id].get('last_play_time', 0)
    current_time = int(time.time())
    time_diff = current_time - last_play_time
    if time_diff < 10 * 60:
        remaining = 10 * 60 - time_diff
        minutes = remaining // 60
        seconds = remaining % 60
        formatted_time = f"{minutes:02}:{seconds:02}"
        await event.reply(f"يجب عليك الانتظار {formatted_time} قبل التداول مجددًا.")
        await react(event, '😐')
        return
    if user_id not in points:
        await event.reply("ماعندك فلوس 💔.")
        await react(event, '💔')
        return
    user_points = points[user_id]
    if user_points < 1000:
        await event.reply(
            f"ماتكدر تتداول حاليا 💔\n"
            f"رصيدك الحالي {user_points} نقطة.\n"
            f"يجب أن يكون رصيدك 1000 نقطة على الأقل للتداول."
        )
        await react(event, '😁')
        return
    f = user_points // 5
    r = random.randint(-50, 75)
    if r > 0:
        profit = int(f * (100 + r) / 100)
        points[user_id] += profit
        await event.reply(
            f"تم التداول بنجاح \n نسبة نجاح {r}% \n فلوس الربح `{profit}` نقطة 🎉\n"
        )
        await react(event, '🎉')
    else:
        loss = int(f * (100 + r) / 100)
        points[user_id] -= abs(loss)
        await event.reply(
            f"تداول بنسبة فاشلة {r}% \n خسرت `{abs(loss)}` نقطة 💔\n"
        )
        await react(event, '😁')
    user_data['تداول'][user_id]['last_play_time'] = current_time
    save_user_data(user_data)
USER_DATA_FILE = "boxing.json"
def load_user_data():
    if os.path.exists(USER_DATA_FILE):
        with open(USER_DATA_FILE, "r", encoding="utf-8") as file:
            return json.load(file)
    return {}
def save_user_data(data):
    with open(USER_DATA_FILE, "w", encoding="utf-8") as file:
        json.dump(data, file, ensure_ascii=False, indent=4)
@ABH.on(events.NewMessage(pattern=r'مضاربة (\d+)'))
async def boxing(event):
    if not event.is_group:
        return
    type = "مضاربة"
    await botuse(type)
    reply = await event.get_reply_message()
    if not reply:
        await event.reply('عزيزي، لازم ترد على رسالة الشخص اللي تريد تضاربه.')
        await react(event, '🤔')
        return
    try:
        count = int(event.pattern_match.group(1)) or points[str(event.sender_id)]
    except ValueError:
        await event.reply('تأكد من كتابة رقم صحيح بعد كلمة مضاربة.')
        await react(event, '🤔')
        return
    user1_id = reply.sender_id
    user2_id = event.sender_id
    gid = str(event.chat_id)
    user_data = load_user_data()
    current_time = int(time.time())
    last_target_time = user_data.get(str(user1_id), {}).get("boxed", 0)
    if current_time - last_target_time < 10 * 60:
        remaining = 10 * 60 - (current_time - last_target_time)
        minutes = remaining // 60
        seconds = remaining % 60
        s = await event.get_sender()
        x = await ment(s)
        rx = await ment(reply)
        await event.reply(f"عزيزي {x} لا يمكنك مضاربة {rx} انتظر {minutes:02}:{seconds:02} دقيقة.")
        await react(event, '😐')
        return
    last_attack_time = user_data.get(str(user2_id), {}).get("attacked", 0)
    if current_time - last_attack_time < 10 * 60:
        remaining = 10 * 60 - (current_time - last_attack_time)
        minutes = remaining // 60
        seconds = remaining % 60
        await event.reply(f"يجب عليك الانتظار {minutes:02}:{seconds:02} قبل أن تبدأ مضاربة جديدة.")
        await react(event, '😐')
        return
    if str(user1_id) not in points:
        await event.reply('الشخص الذي تم الرد عليه لا يملك نقاط.')
        await react(event, '💔')
        return
    if str(user2_id) not in points:
        await event.reply('أنت لا تملك نقاط.')
        await react(event, '😐')
        return
    mu1 = points[str(user1_id)]
    mu2 = points[str(user2_id)]
    if count > mu1:
        await event.reply('فلوس الشخص الذي تم الرد عليه أقل من مبلغ المضاربة.')
        await react(event, '😐')
        return
    if count > mu2:
        await event.reply('فلوسك أقل من مبلغ المضاربة.')
        await react(event, '😁')
        return
    user1_entity = await ABH.get_entity(user1_id)
    user2_entity = await ABH.get_entity(user2_id)
    mention1 = f"[{user1_entity.first_name}](tg://user?id={user1_id})"
    mention2 = f"[{user2_entity.first_name}](tg://user?id={user2_id})"
    winner_id = random.choice([user1_id, user2_id])
    loser_id = user2_id if winner_id == user1_id else user1_id
    points[str(winner_id)] += count
    points[str(loser_id)] -= count
    with open("points.json", "w", encoding="utf-8") as f:
        json.dump(points, f, ensure_ascii=False, indent=2)
    winner_name = mention1 if winner_id == user1_id else mention2
    await event.reply(
        f"🥊 تمت المضاربة!\n\n"
        f"👤 {mention2} 🆚 {mention1}\n\n"
        f"🏆 الفائز: {winner_name}\n"
        f"💰 الجائزة: {count} نقطة 🎉"
    )
    await react(event, '🎉')
    user_data[str(user1_id)] = user_data.get(str(user1_id), {})
    user_data[str(user1_id)]["boxed"] = current_time
    user_data[str(user2_id)] = user_data.get(str(user2_id), {})
    user_data[str(user2_id)]["attacked"] = current_time
    save_user_data(user_data)
spam_file = "spam.json"
if not os.path.exists(spam_file):
    with open(spam_file, 'w', encoding='utf-8') as f:
        json.dump({}, f, ensure_ascii=False, indent=4)
def load_spam():
    try:
        with open(spam_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
            if isinstance(data, dict):
                return data
            else:
                return {}
    except (FileNotFoundError, json.JSONDecodeError):
        return {}
def spam(data):
    with open(spam_file, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)
sessions = {}
emoji = [
    "🤣", "❤️", "👍", "👎", "🔥", "🥰", "👏", "😁", "🤔", "🤯", "😱", "🤬", "😡", "😢", "🎉", "🤩", "🤮", "💩", "🙏", "👌", "🕊",
    "🤡", "🥱", "☺️", "😍", "🐳", "❤️‍🔥", "🌚", "🌭", "😙", "💯", "⚡️", "🍌", "🏆", "😡", "😘", "🙊", "😎", "👾", "🤷‍♂️",
    "🤷‍♀️", "🤷", "☃️", "🗿", "🆒", "💘", "🙈", "😇", "😨", "🤝", "✍️", "🤗", "🫡", "🎅", "🎄", "😴", "😭", "🤓", "👻",
    "👨‍💻", "👀", "🎃", "🙈", "💔", "🤨", "😐", "🍓", "🍾", "💋", "🖕", "😈"
]
@ABH.on(events.NewMessage(pattern=r'^ازعاج(?:\s+(\d{1,2}))?(?:\s+(.+))?$'))
async def handle_spam(event):
    if not event.is_group:
        return
    await botuse("ازعاج")
    data = load_spam()
    gid = str(event.chat_id)
    r = await event.get_reply_message()
    if not r:
        await react(event, "🤔")
        await chs(event, "استخدم الامر ك `ازعاج 4 🌚` \n ثم رد علئ رسالة")
        return
    if gid in data and str(r.sender_id) in data[gid]:
        await chs(event, 'كعد ازعجه هذا الخسيس من اكمل ذكرني ازعجه الك ')
        return
    much = event.pattern_match.group(1)
    text = event.pattern_match.group(2)
    gid = str(event.chat_id)
    id = str(event.sender_id)
    if not r:
        await react(event, "🤔")
        await chs(event, "اكتب `ازعاج 4 🌚 وسوي رد `")
        return
    if not much or not text:
        await react(event, "🤔")
        await chs(event, "استخدم الامر ك `ازعاج 4 🌚`")
        return
    if not much.isdigit() or int(much) < 1 or int(much) > 50 and id != wfffp:
        await react(event, "🤔")
        await chs(event, "عدد مرات الازعاج يجب ان يكون بين 1 و 50")
        return
    if not text:
        await react(event, "🤔")
        await chs(event, "حدد الايموجي اللي تريده")
        return
    if len(text) > 1:
        await react(event, "🤔")
        await chs(event, "عذرا بس ماكدر اسويله اكثر من ايموجي واحد")
        return
    if text not in emoji:
        await react(event, "🤔")
        await chs(event, f"الايموجي {text} مدعوم الايموجيات المدعومة هي:\n" + " ".join(emoji)
        )
        return
    much = int(much)
    uid = (await ABH.get_me()).id
    if r.sender_id == uid:
        await react(event, "🤔")
        await chs(event, "لا يمكنك ازعاجي 😒")
        return
    if r.sender_id == event.sender_id:
        await react(event, "🤔")
        await chs(event, "لا يمكنك ازعاج نفسك 😁")
        return
    if r.sender_id == wfffp:
        await react(event, "🤔")
        await chs(event, "لا يمكنك ازعاج عمك 😒")
        return
    if r.sender.bot:
        await react(event, "🤔")
        await chs(event, "لا يمكنك ازعاج البوتات 😒")
        return
    a = auth(event, True)
    #if a:
        #await chs(event, f"عذرا ماتكدر تزعج ( {await ment(r)} )")
        #return
    uid = str(event.sender_id)
    gid = str(event.chat_id)
    if uid in points:
        m = points[uid]
    else:
        m = 0
    ء = much * 50000
    if m < 50000:
        await react(event, "🤣")
        await chs(event, f"فلوسك اقل من 50 الف دينار ماكدر تسوي ازعاج واحد اصلا")
        return
    if ء > m:
        await react(event, "🤣")
        await chs(event, f"فلوسك {m} دينار وتحتاج {much / 50000} حتى تسوي {much} ازعاج.")
        return
    b = [Button.inline("نعم", b"yes"), Button.inline("لا", b"no")]
    await event.respond(f'هل تريد ازعاج {much} مرات بـ "{text}"؟\n\nسيتم خصم {ء} نقاط من رصيدك.', buttons=[b], reply_to=event.id)
    if gid not in sessions:
        sessions[gid] = {}
    sessions[gid][id] = {
        "much": much,
        "text": text,
        "id": r.sender_id,
        "reply_to": event.id
    }
@ABH.on(events.CallbackQuery(data=b"yes"))
async def confirm_spam(event):
    gid = str(event.chat_id)
    uid = str(event.sender_id)
    d = load_spam()
    if gid in sessions and uid in sessions[gid]:
        data = sessions[gid][uid]
        if not data:
            await event.answer("انتهت الجلسة (بيانات ناقصة)", alert=True)
            return
        much = data.get("much")
        text = data.get("text")
        rid = str(data.get("id"))
        reply_to = data.get("reply_to")
        if not all([much, text, rid]):
            await event.answer("انتهت الجلسة (قيمة ناقصة)", alert=True)
            return
        await event.edit(f'تم تفعيل الازعاج {much} مرات بـ "{text}"')
        delpoints(event.sender_id, event.chat_id, points, much * 50000)
        if gid not in d:
            d[gid] = {}
        d[gid][rid] = {
            "text": text,
            "count": much,
            "reply_to": reply_to
        }
        spam(d)
        del sessions[gid][uid]
    else:
        await event.answer("انتهت جلسة الازعاج", alert=True)
@ABH.on(events.CallbackQuery(data=b"no"))
async def cancel_spam(event):
    event.edit("تم إلغاء الازعاج")
    del sessions[event.chat_id][event.sender_id]
@ABH.on(events.NewMessage)
async def monitor_messages(event):
    if not event.is_group:
        return
    data = load_spam()
    gid = str(event.chat_id)
    uid = str(event.sender_id)  
    if gid in data and uid in data[gid]:
        info = data[gid][uid]
        text = info.get('text', '🌚')
        count = info.get('count', 0)
        if text and count > 0:
            await react(event, text)
            data[gid][uid]['count'] = count - 1
            if data[gid][uid]['count'] <= 0:
                del data[gid][uid]
                if not data[gid]:
                    del data[gid]
            spam(data)
@ABH.on(events.NewMessage(pattern='^/dates|مواعيد$'))
async def show_dates(event):
    if not event.is_group:
        return
    global uid, msg
    type = "مواعيد"
    await botuse(type)
    btton = [[
        Button.inline("محرم", b"mh"),
        Button.inline("رمضان", b"rm"),
        Button.inline("شعبان", b"sh"),
        Button.inline("رجب", b"r"),
        Button.inline("حدد تاريخ", b"set_date")
    ]]
    msg = await event.respond("اختر الشهر المناسب أو حدد تاريخ خاص 👇", buttons=btton, reply_to=event.id)
    uid = event.sender_id
@ABH.on(events.CallbackQuery(data='set_date'))
async def set_date(event):
    المرسل_الثاني = event.sender_id
    if المرسل_الثاني != uid:
        await event.answer('عزيزي الامر لا يخصك', alert=True)
        return
    await event.edit("من فضلك أدخل التاريخ بصيغة YYYY-MM-DD مثال: 2025-06-15", buttons=None)
@ABH.on(events.CallbackQuery(data='mh'))
async def handle_mh(event):
    x = (2026, 6, 17)
    الان = datetime.today()
    x_datetime = datetime(*x)
    الباقي = x_datetime - الان
    await event.edit(f'باقي {الباقي.days} لمحرم يوم', buttons=None)
@ABH.on(events.CallbackQuery(data='rm'))
async def handle_rm(event):
    x = (2026, 2, 22)
    الان = datetime.today()
    x_datetime = datetime(*x)
    الباقي = x_datetime - الان
    await event.edit(f'باقي {الباقي.days} لرمضان يوم', buttons=None)
@ABH.on(events.CallbackQuery(data='sh'))
async def handle_sh(event):
    x = (2026, 1, 22)
    الان = datetime.today()
    x_datetime = datetime(*x)
    الباقي = x_datetime - الان
    await msg.edit(f'باقي {الباقي.days} لشعبان يوم', buttons=None)
@ABH.on(events.CallbackQuery(data='r'))
async def handle_r(event):
    x = (2025, 12, 22)
    الان = datetime.today()
    x_datetime = datetime(*x)
    الباقي = x_datetime - الان
    await event.edit(f'باقي {الباقي.days} لرجب يوم', buttons=None)
@ABH.on(events.NewMessage(pattern=r'^\d{4}-\d{2}-\d{2}$'))
async def set_user_date(event):
    user_id = event.sender_id
    date = event.text
    try:
        datetime.strptime(date, "%Y-%m-%d")
        save_date(user_id, date)
        await event.reply(f"تم حفظ التاريخ {date}. يمكنك الآن معرفة كم باقي.")
    except ValueError:
        await event.reply("التاريخ المدخل غير صالح، يرجى إدخاله بصيغة YYYY-MM-DD.")
@ABH.on(events.NewMessage(pattern='^كم باقي$'))
async def check_remaining_days(event):
    if not event.is_group:
        return
    type = "كم باقي"
    await botuse(type)
    user_id = event.sender_id
    saved_date = get_saved_date(user_id)
    if saved_date:
        t = datetime.today()
        saved_date_obj = datetime.strptime(saved_date, "%Y-%m-%d").date()
        days_difference = (saved_date_obj - t.date()).days
        msg = f"باقي {days_difference} ايام" if days_difference >= 0 else f"التاريخ قد مضى منذ {abs(days_difference)} يوم"
        await event.reply(msg)
    else:
        await event.reply("لم تحدد تاريخًا بعد، يرجى تحديد تاريخ أولاً.")
@ABH.on(events.NewMessage(pattern='^تاريخ$'))
async def today(event):
    if not event.is_group:
        return
    type = "تاريخ"
    await botuse(type)
    tt = datetime.now().date()
    tt_minus_one = tt - timedelta(days=1)
    hd = Gregorian(tt_minus_one.year, tt_minus_one.month, tt_minus_one.day).to_hijri()
    hd_str = f"{hd.day} {hd.month_name('ar')} {hd.year} هـ"
    await event.reply(f"الهجري: \n{hd_str} \nالميلادي: \n{tt}")
@ABH.on(events.NewMessage(pattern=r'كشف ايدي (\d+)'))
async def link(event):
    if not event.is_group:
        return
    type = "كشف ايدي"
    await botuse(type)
    global user
    user_id = event.pattern_match.group(1)
    if not user_id:
        await event.reply("استخدم الأمر كـ `كشف ايدي 1910015590`")
        return
    try:
        user = await event.client.get_entity(int(user_id))
    except:
        return await event.reply(f"لا يوجد حساب بهذا الآيدي...")
    tag = await ment(user)
    button = [Button.inline("تغيير إلى رابط", b"recgange")]
    await event.reply(f"⌔︙{tag}", buttons=[button])
@ABH.on(events.CallbackQuery(data=b"recgange"))
async def chang(event):
    await asyncio.sleep(2)
    await event.edit(f"⌔︙رابط المستخدم: tg://user?id={user.id}")
@ABH.on(events.NewMessage(pattern=r'(ترجمة|ترجمه)'))
async def translation(event):
    if not event.is_group:
        return
    type = "ترجمة"
    await botuse(type)
    translator = Translator()
    if event.is_reply:
        replied_message = await event.get_reply_message()
        original_text = replied_message.text 
    else:
        command_parts = event.message.text.split(' ', 1)
        original_text = command_parts[1] if len(command_parts) > 1 else None
    if not original_text:
        await event.reply("يرجى الرد على رسالة تحتوي على النص المراد ترجمته أو كتابة النص بجانب الأمر.")
        
        return
    detected_language = translator.detect(original_text)
    if detected_language.lang == "ar": 
        translated = translator.translate(original_text, dest="en")
    else: 
        translated = translator.translate(original_text, dest="ar")
    response = (
        f"اللغة المكتشفة: {detected_language.lang}\n"
        f"النص المترجم: `{translated.text}`"
    )
    await event.reply(response)
rights_translation = {
    "change_info": "تغيير معلومات المجموعة",
    "ban_users": "حظر الأعضاء",
    "invite_users": "دعوة أعضاء",
    "pin_messages": "تثبيت الرسائل",
    "add_admins": "إضافة مشرفين",
    "manage_call": "إدارة المكالمات الصوتية",
    "anonymous": "الوضع المتخفي",
    "manage_topics": "إدارة المواضيع",
}
def translate_rights_lines(rights_obj):
    lines = []
    for key, name in rights_translation.items():
        status = getattr(rights_obj, key, False)
        emoji = "👍🏾" if status else "👎🏾"
        lines.append(f"{emoji} ⇜ {name}")
    return "\n".join(lines) if lines else "لا يوجد صلاحيات"
@ABH.on(events.NewMessage(pattern=r'^صلاحياته(?: (.+))?$'))
async def his_rights(event):
    if not event.is_group:
        return
    type = "صلاحياته"
    await botuse(type)
    try:
        chat = await event.get_input_chat()
        match = event.pattern_match.group(1)
        if match:
            target = match
        else:
            reply = await event.get_reply_message()
            if not reply:
                await event.reply("استخدم الرد على رسالة المستخدم أو أرسل معرفه بعد الأمر.")
                return
            target = reply.sender_id
        result = await ABH(GetParticipantRequest(channel=chat, participant=target))
        translated = translate_rights_lines(result.participant.admin_rights)
        await event.reply(f"صلاحياته\n{translated}")
    except Exception:
        await event.reply("لا يمكن عرض الصلاحيات.")
@ABH.on(events.NewMessage(pattern=r'^لقبه(?: (.+))?$'))
async def nickname_r(event):
    if not event.is_group:
        return
    type = "لقبه"
    await botuse(type)
    try:
        chat = await event.get_input_chat()
        match = event.pattern_match.group(1)
        if match:
            target = match
        else:
            reply = await event.get_reply_message()
            if not reply:
                await event.reply("استخدم الرد على رسالة المستخدم أو أرسل معرفه بعد الأمر.")
                return
            target = reply.sender_id
        result = await ABH(GetParticipantRequest(channel=chat, participant=target))
        participant = result.participant
        nickname = getattr(participant, 'rank', None) or "مشرف"
        await event.reply(f"لقبه ↞ {nickname}")
    except Exception:
        await event.reply("المستخدم ليس مشرفًا أو لا يمكن العثور عليه.")
p = ["تاريخه", 'تاريخ انضمامه', 'تاريخ انضمامه']
@ABH.on(events.NewMessage(pattern=r'^تاريخي|انضمامي|تاريخ انضمامي|تاريخه|تاريخ انضمامه|تاريخ انضمامه$'))
async def my_date(event):
    if not event.is_group:
        return
    text = event.text
    target = event.sender_id
    if text in p:
        r = event.get_reply_message()
        target = r.sender_id
        return
    await botuse(text)
    chat = await event.get_input_chat()
    result = await ABH(GetParticipantRequest(channel=chat, participant=target))
    participant = result.participant
    date_joined = participant.date.strftime("%Y-%m-%d %H:%M")
    await event.reply(f"تاريخ الانضمام ↞ {date_joined}")
@ABH.on(events.NewMessage(pattern=r'^(اقرا|اقرأ|كم الرقم|اقرأ الرقم) (\d+)$'))
async def readnum(e):
    num = e.pattern_match.group(2)
    try:
        number = num2words(num, lang='ar')
        await chs(e, f'الرقم {num} يُقرأ كـ:\n{number}')
    except Exception as e:
        await hint(f'{e}')
