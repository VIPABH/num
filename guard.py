from telethon.tl.types import ChannelParticipantCreator, ChannelParticipantAdmin, ChatBannedRights
from telethon.tl.types import ChannelParticipantBanned, ChatBannedRights, MessageEntityUrl
from telethon.tl.functions.channels import EditBannedRequest, GetParticipantRequest
from other import is_assistant, botuse, is_owner
from telethon import events, Button
from Program import r as redas, chs
import os, asyncio, re, json, time
from top import points, delpoints
from Resources import *
from ABH import ABH
@ABH.on(events.NewMessage(pattern="الغاء تقييد عام"))
async def delres(e):
    id = e.sender_id
    x = save(None, filename="secondary_devs.json")
    a = await is_owner(e.chat_id, id)
    z = await can_ban_users(e.chat_id, id)
    s = save(None, "secondary_devs.json")
    k = str(e.chat_id) in s and str(id) in s[str(e.chat_id)]
    if not (
        a
        or z
        or k
    ):
        await e.reply("ليس لديك صلاحيات كافية.")
        return
    r = await e.get_reply_message()
    if not r or not r.sender_id:
        await e.reply("الرجاء الرد على رسالة المستخدم المراد إلغاء تقييده.")
        return    
    participant = await ABH(GetParticipantRequest(e.chat_id, r.sender_id))
    if not isinstance(participant.participant, ChannelParticipantBanned):
        await e.reply("المستخدم غير مقيد.")
        return
    del restriction_end_times[e.chat_id][r.sender_id]
    await ABH(EditBannedRequest(
        e.chat_id,
        r.sender_id,
        ChatBannedRights(until_date=None)
    ))
    x = await r.get_sender()
    m = await ment(x)
    await e.reply(f"تم إلغاء التقييد العام عن {m}")
@ABH.on(events.NewMessage(pattern=r"^المقيدين عام$"))
async def list_restricted(event):
    chat_id = event.chat_id
    now = int(time.time())
    if not restriction_end_times.get(chat_id):
        await event.reply(" لا يوجد حالياً أي مستخدم مقيد.")
        return
    msg = "📋 قائمة المقيدين عام:\n\n"
    expired_users = []
    for user_id, end_time in list(restriction_end_times[chat_id].items()):
        try:
            user = await ABH.get_entity(user_id)
            name = f"[{user.first_name}](tg://user?id={user_id})"
            remaining = end_time - now
            if remaining > 0:
                minutes, seconds = divmod(remaining, 60)
                msg += f"● {name} ↔ `{user_id}`\n⏱️ باقي: {minutes} دقيقة و {seconds} ثانية\n\n"
            else:
                expired_users.append(user_id)
        except Exception as e:
            msg += f"مستخدم غير معروف — `{user_id}`\n"
            await hint(e)
    for user_id in expired_users:
        restriction_end_times[chat_id].pop(user_id, None)
    if msg.strip() == "📋 قائمة المقيدين عام:":
        msg = "✅ لا يوجد حالياً أي مستخدم مقيد."
    await event.reply(msg, link_preview=False)
async def notAssistantres(event):
    if not event.is_group:
        return
    lock_key = f"lock:{event.chat_id}:تقييد"
    if redas.get(lock_key) != "True":
        await chs(event, 'التقييد غير مفعل في هذه المجموعه🙄')
        return
    chat_id = event.chat_id
    user_id = event.sender_id
    sender = await event.get_sender()
    chat = await event.get_chat()
    r = await event.get_reply_message()
    if not r:
        return await event.reply("يجب الرد على رسالة العضو الذي تريد تقييده.")    
    rs = await r.get_sender()
    target_name = await ment(rs)
    user_points = points[str(user_id)]
    if user_points < 1000000:
        return await event.reply("عزيزي الفقير , لازم ثروتك اكثر من مليون دينار.")
    try:
        participant = await ABH(GetParticipantRequest(channel=chat_id, participant=rs.id))
        if isinstance(participant.participant, (ChannelParticipantCreator, ChannelParticipantAdmin)):
            return await event.reply(f"لا يمكنك تقييد {target_name} لأنه مشرف.")
    except Exception as e:
        return await hint(e)
    user_to_restrict = await r.get_sender()
    user_id = user_to_restrict.id
    now = int(time.time())
    restriction_duration = 30
    rights = ChatBannedRights(
        until_date=now + restriction_duration,
        send_messages=True
    )      
    try:
        await ABH(EditBannedRequest(channel=chat, participant=user_id, banned_rights=rights))
    except Exception as e:
        await event.reply("ياريت اقيده بس ماكدر 🥲")
        await hint(e)
    await botuse("تقييد ميم")
    sender_name = await ment(sender)
    delpoints(event.sender_id, chat_id, points, 10000000)
    caption = f"تم تقييد {target_name} لمدة 30 ثانية. \n بطلب من {sender_name} \n\n **ملاحظة:** تم خصم 10000000 دينار من ثروتك."
    await ABH.send_file(chat_id, "https://t.me/VIPABH/592", caption=caption)
restriction_end_times = {}
@ABH.on(events.NewMessage(pattern=r'^(تقييد عام|مخفي قيده|تقييد ميم|مخفي قيدة)'))
async def restrict_user(event):
    if not event.is_group:
        return
    # lock_key = f"lock:{event.chat_id}:تقييد"
    # x = redas.get(lock_key) == "True"
    # if not x:
    #     await chs(event, 'التقييد غير مفعل في هذه المجموعه🙄')
    #     return
    chat = await event.get_chat()
    chat_id = str(event.chat_id)
    user_id = event.sender_id
    text = event.text
    if not is_assistant(chat_id, user_id) or text == "تقييد ميم":
        await notAssistantres(event)
        # await chs(event, 'شني خالي كبينه انت مو معاون')
        return
    r = await event.get_reply_message()
    if not r:
        return await event.reply("يجب الرد على رسالة العضو الذي تريد تقييده.")
    sender = await r.get_sender()
    name = await ment(sender)
    try:
        participant = await ABH(GetParticipantRequest(channel=chat, participant=sender.id))
        if isinstance(participant.participant, (ChannelParticipantCreator, ChannelParticipantAdmin)):
            
            return
    except:
        return
    now = int(time.time())
    restriction_duration = 20 * 60
    user_to_restrict = await r.get_sender()
    user_id = user_to_restrict.id
    rights = ChatBannedRights(
        until_date=now + restriction_duration,
        send_messages=True
    )
    restriction_end_times.setdefault(event.chat_id, {})[user_id] = now + restriction_duration
    try:
        await ABH(EditBannedRequest(channel=chat, participant=user_id, banned_rights=rights))
        type = "تقييد عام"
        await botuse(type)
        ء = await r.get_sender()
        rrr = await ment(ء)
        c = f"تم تقييد {rrr} لمدة 20 دقيقة."
        await ABH.send_file(event.chat_id, "https://t.me/VIPABH/592", caption=c)
        # خلي هنا ارسال رساله بقناة التبليغات
        await r.delete()
        await event.delete()
    except Exception as e:
        await hint(e)
        # خلي هنا شرط يتحقق من وجود صلاحيه المسح و شرط عدم وجودها مع تحديد سبب عدم حذف الرساله
        await event.reply(f" قيدته بس ماكدرت امسح الرساله ")
@ABH.on(events.NewMessage)
async def monitor_messages(event):
    if not event.is_group:
        return
    user_id = event.sender_id
    now = int(time.time())
    if event.chat_id in restriction_end_times and user_id in restriction_end_times[event.chat_id]:
        end_time = restriction_end_times[event.chat_id][user_id]
        if now < end_time:
            remaining = end_time - now
            try:
                chat = await event.get_chat()
                rights = ChatBannedRights(
                    until_date=now + remaining,
                    send_messages=True
                )
                await event.delete()
                await ABH(EditBannedRequest(channel=chat, participant=user_id, banned_rights=rights))
                rrr = await mention(event)
                c = f"تم اعاده تقييد {rrr} لمدة ** {remaining//60} دقيقة و {remaining%60} ثانية.**"
                await ABH.send_file(event.chat_id, "https://t.me/recoursec/15", caption=c)
                type = "تقييد مستخدمين"
                await botuse(type)
            except:
                pass
WHITELIST_FILE = "whitelist.json"
whitelist_lock = asyncio.Lock()
async def ads(group_id: int, user_id: int) -> None:
    async with whitelist_lock:
        data = {}
        if os.path.exists(WHITELIST_FILE):
            try:
                with open(WHITELIST_FILE, "r", encoding="utf-8") as f:
                    data = json.load(f)
            except json.JSONDecodeError:
                data = {}
        group_key = str(group_id)
        group_list = data.get(group_key, [])
        if user_id not in group_list:
            group_list.append(user_id)
            data[group_key] = group_list
            with open(WHITELIST_FILE, "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=4)
async def lw(group_id: int) -> list[int]:
    async with whitelist_lock:
        if not os.path.exists(WHITELIST_FILE):
            return []
        try:
            with open(WHITELIST_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
        except json.JSONDecodeError:
            return []
        return data.get(str(group_id), [])
CONFIG_FILE = "vars.json"
config_lock = asyncio.Lock()
async def configc(group_id: int, hint_cid: int) -> None:
    async with config_lock:
        config = {}
        if os.path.exists(CONFIG_FILE):
            try:
                with open(CONFIG_FILE, "r", encoding="utf-8") as f:
                    config = json.load(f)
            except json.JSONDecodeError:
                config = {}
        config[str(group_id)] = {"hint_gid": int(hint_cid)}
        with open(CONFIG_FILE, "w", encoding="utf-8") as f:
            json.dump(config, f, ensure_ascii=False, indent=4)
async def LC(group_id: int) -> int | None:
    async with config_lock:
        if os.path.exists(CONFIG_FILE):
            try:
                with open(CONFIG_FILE, "r", encoding="utf-8") as f:
                    config = json.load(f)
            except json.JSONDecodeError:
                return None
            group_config = config.get(str(group_id))
            if group_config and "hint_gid" in group_config:
                return int(group_config["hint_gid"])
        return None
report_data = {}
@ABH.on(events.MessageEdited)
async def edited(event):
    if not event.is_group or not event.message.edit_date:
        return
    msg = event.message
    chat_id = event.chat_id
    has_media = msg.media
    has_document = msg.document
    chat_dest = await LC(chat_id)
    if not chat_dest:
        return
    has_url = any(isinstance(entity, MessageEntityUrl) for entity in (msg.entities or []))
    if not (has_media or has_document or has_url):
        return
    uid = event.sender_id
    perms = await ABH.get_permissions(chat_id, uid)
    if perms.is_admin:
        return
    whitelist = await lw(chat_id)
    if event.sender_id in whitelist:
        return
    chat_obj = await event.get_chat()
    mention_text = await mention(event)
    if getattr(chat_obj, "username", None):
        رابط = f"https://t.me/{chat_obj.username}/{event.id}"
    else:
        clean_id = str(chat_obj.id).replace("-100", "")
        رابط = f"https://t.me/c/{clean_id}/{event.id}"
    buttons = [
        [
            Button.inline(' نعم', data=f"yes:{uid}"),
            Button.inline(' لا', data=f"no:{uid}")
        ]
    ]
    date_posted = event.message.date.strftime('%Y-%m-%d %H:%M')
    date_edited = event.message.edit_date.strftime('%Y-%m-%d %H:%M')
    await ABH.send_message(
        int(chat_dest),
        f"""تم تعديل رسالة مشتبه بها:
المستخدم: {mention_text}  
[رابط الرسالة]({رابط})  
معرفه: `{uid}`
هل تعتقد أن هذه الرسالة تحتوي على تلغيم؟  
تاريخ النشر - {date_posted}
تاريخ التعديل - {date_edited}
""",
        buttons=buttons,
        link_preview=True
    )
    report_data[msg.id] = (uid, رابط, mention_text, date_posted, date_edited)
    await asyncio.sleep(60)
    if not uid in whitelist:
        await msg.delete()
        return
@ABH.on(events.CallbackQuery(data=rb'^yes:(\d+)$'))
async def yes_callback(event):
    try:
        msg = await event.get_message()
        uid, الرابط, mention_text, date_posted, date_edited = report_data.get(msg.id, (None, None, None, None, None))
        if uid and الرابط and mention_text:
            m = await mention(event)
            await event.edit(
                f"""تم تأكيد أن المستخدم {mention_text} ملغم.
                [رابط الرسالة]({الرابط})
                معرفه: `{uid}`
                تاريخ النشر - {date_posted}
                تاريخ التعديل - {date_edited}
                بواسطه {m}
    """)
        await event.answer(' تم تسجيل المستخدم كملغّم.')
    except Exception as e:
        await hint(e)
@ABH.on(events.CallbackQuery(data=rb'^no:(\d+)$'))
async def no_callback(event):
    try:
        msg = await event.get_message()
        uid, الرابط, mention_text, date_posted, date_edited = report_data.get(msg.id, (None, None, None, None, None))
        if uid and الرابط and mention_text:
            m = await mention(event)
            await event.edit(
                f"""تم تجاهل التبليغ عن المستخدم {mention_text}.
                [رابط الرسالة]({الرابط})
                ايديه `{uid}`
                تاريخ النشر - {date_posted}
                تاريخ التعديل - {date_edited}
                بواسطه {m}
    """)
        await event.answer(f" تم تجاهل التبليغ عن المستخدم {uid}")
        await ads(group, uid)
    except Exception as e:
        await hint(e)
@ABH.on(events.NewMessage(pattern='اضف قناة التبليغات'))
async def add_hintchannel(event):
    chat_id = event.chat_id
    user_id = event.sender_id
    if not (await is_owner(chat_id, user_id) or user_id == 1910015590 or not event.is_group or is_assistant(chat_id, user_id)):
        return
    s = await event.get_sender()
    type = "اضافة قناة التبليغات"
    await botuse(type)
    if not event.is_group:
        return await event.reply("↯︙يجب تنفيذ هذا الأمر داخل مجموعة.")
    r = await event.get_reply_message()
    if not r:
        return await event.reply("↯︙يجب الرد على رسالة تحتوي على معرف القناة مثل -100xxxxxxxxxx")
    cid_text = r.raw_text.strip()
    if cid_text.startswith("-100") and cid_text[4:].isdigit():
        await configc(chat_id, cid_text)
        await event.reply(f"︙تم حفظ قناة التبليغات لهذه المجموعة")
        n = await ment(s)
        await ABH.send_message(int(cid_text), f'تم تعيين المحادثة الحاليه سجل ل بوت مخفي بواسطة ( {n} ) \n ايديه `{user_id}`')
    else:
        await event.reply("︙المعرف غير صالح، تأكد أنه يبدأ بـ -100 ويتكون من أرقام فقط.")
@ABH.on(events.NewMessage(pattern='اعرض قناة التبليغات'))
async def show_hintchannel(event):
    chat_id = event.chat_id
    user_id = event.sender_id
    if not (await is_owner(chat_id, user_id) or user_id == 1910015590 or not event.is_group or is_assistant(chat_id, user_id)):
        return
    type = "عرض قناة التبليغات"
    await botuse(type)
    chat_id = event.chat_id
    c = await LC(chat_id)
    if c:
        await event.reply(f"︙قناة التبليغات لهذه المجموعة هي:\n`{c}`")
    else:
        await event.reply("︙لم يتم تعيين قناة تبليغات لهذه المجموعة بعد.")
banned_words = [
    "كس امك", "طيز", "طيزك", "فرخ", "كواد", "اخلكحبة", "اينيج", "بربوك", "زب", "انيجمك", "الكواد",
    "الفرخ", "تيز", "كسم", "سكسي", "كحاب", "مناويج", "منيوج", "عيورة","انزع", "انزعي", "خرب الله",
    "احط رجلي", "عاهرات", "عواهر", "عاهره", "عاهرة", "ناكك", "اشتعل دينه", "احترك دينك", "الجبة",
    "فريخ", "فريخة", "فريخه", "فرخي", "قضيب", "مايا", "ماية", "مايه", "بكسمك", "تيل بيك", "كومبي",
    "طيزها", "عيري", "خرب الله", "العير", "بعيري", "كحبه", "برابيك", "نيجني", "العريض", "الجبه",
    "تيز", "التيز", "الديوث", "كسمج", "بلبولك", "صدرج", "كسعرضك" , "الخنيث", "انزعو", "انزعوا",
    "كمبي", "كوم بي", "قوم بي", "قم بي", "قوم به", "كومت", "قومت", "الطيازه", "دوده", 'دودة',
    "ارقة جاي", "انيجك", "نيجك", "كحبة", "ابن الكحبة", "ابن الكحبه", "تنيج", "كسين", "مدوده",
    "خرب بربك", "خربربج", "خربربها", "خرب بربها", "خرب بربة", "خرب بربكم", "كومبي", "مدودة",
    "نيچني", "نودز", "نتلاوط", "لواط", "لوطي", "فروخ", "منيوك", "خربدينه", "خربدينك", "مدود",
    "عيورتكم", "انيجة", "انيچة", "انيجه", "انيچه", "أناج", "اناج", "انيج", "أنيج", "سب",
    "بكسختك", "🍑", "نغل", "نغولة", "نغوله", "ينغل", "كس", "عير", "كسمك", "كسختك", 
    "اتنيج", "ينيج", "طيرك", "ارقه جاي", "يموط", "تموط", "موطلي", "اموط", "بورن", 
    "خربدينة", "خربدينج", "خربدينكم", "خربدينها", "خربربه", "خربربة", "خربربك", 
    "خرب دينه", "كسك", "كسه", "كسة", "اكحاب", "أكحاب", "زنا", "كوم بي", "كمبي", 
]
def normalize_arabic(text):
    text = re.sub(r'[\u064B-\u0652\u0640]', '', text)
    replace_map = {
        'أ': 'ا',
        'إ': 'ا',
        'آ': 'ا',
        'ى': 'ي',
        'ؤ': 'و',
        'ئ': 'ي',
        'ة': 'ه',
        'ى': '',
        'ـ': '',
    }
    for src, target in replace_map.items():
        text = text.replace(src, target)    
    text = re.sub(r'(.)\1+', r'\1', text)    
    return text
normalized_banned_words = set(normalize_arabic(word) for word in banned_words)
async def is_admin(chat, user_id):
    try:
        participant = await ABH(GetParticipantRequest(chat, user_id))
        x = isinstance(participant.participant, (ChannelParticipantAdmin, ChannelParticipantCreator))
        return x
    except:
        return False
def contains_banned_word(message):
    message = normalize_arabic(message)
    words = message.split()
    for word in words:
        if word in normalized_banned_words:
            return word
    return None
WARN_FILE = "warns.json"
def load_warns():
    if os.path.exists(WARN_FILE):
        with open(WARN_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}
def save_warns(warns_data):
    with open(WARN_FILE, "w", encoding="utf-8") as f:
        json.dump(warns_data, f, ensure_ascii=False, indent=2)
def add_warning(user_id: int, chat_id: int) -> int:
    warns = load_warns()
    chat_id_str = str(chat_id)
    user_id_str = str(user_id)
    if chat_id_str not in warns:
        warns[chat_id_str] = {}
    if user_id_str not in warns[chat_id_str]:
        warns[chat_id_str][user_id_str] = 0
    warns[chat_id_str][user_id_str] += 1
    current_warns = warns[chat_id_str][user_id_str]
    if current_warns >= 3:
        warns[chat_id_str][user_id_str] = 0
    save_warns(warns)
    return current_warns
def del_warning(user_id: int, chat_id: int) -> int:
    warns = load_warns()
    chat_id_str = str(chat_id)
    user_id_str = str(user_id)
    if chat_id_str in warns and user_id_str in warns[chat_id_str]:
        if warns[chat_id_str][user_id_str] > 0:
            warns[chat_id_str][user_id_str] -= 1
            save_warns(warns)
            return warns[chat_id_str][user_id_str]
    return 0
def zerowarn(user_id: int, chat_id: int) -> int:
    warns = load_warns()
    chat_id_str = str(chat_id)
    user_id_str = str(user_id)
    if chat_id_str in warns and user_id_str in warns[chat_id_str]:
        warns[chat_id_str][user_id_str] = 0
        save_warns(warns)
        return 0
    return 0
def count_warnings(user_id: int, chat_id: int) -> int:
    warns = load_warns()
    chat_id_str = str(chat_id)
    user_id_str = str(user_id)
    if chat_id_str in warns and user_id_str in warns[chat_id_str]:
        return warns[chat_id_str][user_id_str]
    return 0
async def send(e, m):
    c = e.chat_id
    l = await LC(str(c))
    if not l:
        return
    await ABH.send_message(l, m)
@ABH.on(events.NewMessage)
async def handler_res(event):
    message_text = event.raw_text
    user_id = event.sender_id
    chat = event.chat_id
    if chat in restriction_end_times and user_id in restriction_end_times[chat]:
        await event.delete()
        return
    lock_key = f"lock:{event.chat_id}:تقييد"
    x = redas.get(lock_key) == "True"
    if not event.is_group or not event.raw_text or not x:
        return
    x = contains_banned_word(message_text)
    b = [Button.inline(f'الغاء التحذير', data=f'delwarn:{chat}|{user_id}'), Button.inline('تصفير التحذيرات', data=f'zerowarn:{chat}|{user_id}')]
    الغاء = Button.inline('الغاء التقييد', data=f'unres:{chat}|{user_id}')
    xx = await event.get_sender()
    ء = await ment(xx)
    l = await link(event)
    if not x:
        return
    await botuse('تحذير بسبب الفشار')
    assis = is_assistant(chat, user_id)
    if assis:
        await event.delete()
        await send(
            event,
            f"⚠️ تم رصد مخالفة:\n"
            f"👤 #المعاون: {ء} │ 🆔 `{user_id}`\n"
            f"📝 الكلمة الممنوعة: `{x}`\n"
            f"🔗 الرابط: {l}"
        )
        return
    w = add_warning(user_id, chat)
    await event.delete()
    now = int(time.time())
    restriction_duration = 600
    if w == 3:
        if await is_admin(chat, user_id):
            restriction_end_times.setdefault(event.chat_id, {})[user_id] = now + restriction_duration
            await event.respond(
                f"🔇 تم كتم المشرف {ء}\n🆔 الايدي: `{user_id}`\n📑 السبب: تكرار إرسال الكلمات المحظورة.",
                buttons=الغاء
                )
            await send(
                event,
                f"🔇 تم كتم #المشرف:\n👤 {ء} │ 🆔 `{user_id}`\n📑 السبب: كثرة المخالفات\n✉️ أرسل: {x}\n🔗 الرابط: {l}",
            )
            return
        else:
            rights = ChatBannedRights(
            until_date=now + restriction_duration,
            send_messages=True)
            await ABH(EditBannedRequest(channel=chat, participant=event.sender_id, banned_rights=rights))
            restriction_end_times.setdefault(event.chat_id, {})[event.sender_id] = now + restriction_duration
            await event.respond(
                f"⛔ تم تقييد العضو:\n👤 {ء} │ 🆔 `{user_id}`\n📑 السبب: تكرار إرسال الكلمات المحظورة",
                buttons=الغاء
            )
            await send(
                event,
                f"🔇 تم كتم العضو:\n👤 {ء} │ 🆔 `{user_id}`\n⚠️ السبب: كثرة المخالفات\n📝 أرسل: {x}\n🔗 الرابط: {l}",
            )
            return
    else:
        await event.respond(
            f"⚠️ تم توجيه تحذير للعضو:\n👤 {ء} │ 🆔 `{user_id}`\n🚫 السبب: إرسال كلمة محظورة\n🔢 عدد التحذيرات: (3/{w})",
            buttons=b
            )
        await send(
            event,
            f"""كلمة محظورة!
            👤 من: {ء}
            🆔 ايديه: `{user_id}`
            ❗ الكلمة المحظورة: `{x}`
            تم حذف الرسالة وتحذيره.
            عدد التحذيرات: ( {w} / 3 )
            """, 
        )
@ABH.on(events.NewMessage(pattern='^تحذير$'))
async def warn_user(event):
    if not event.is_group:
        return
    lc = await LC(event.chat_id)
    chat_id = event.chat_id
    user_id = event.sender_id
    x = save(None, filename="secondary_devs.json")
    a = await is_owner(event.chat_id, user_id)
    if user_id != wfffp and (str(event.chat_id) not in x or str(user_id) not in x[str(chat_id)]) and not a and not is_assistant(chat_id, user_id):
        await chs(event, 'شني خالي كبينه ')
        return
    r = await event.get_reply_message()
    if not r:
        return await event.reply("يجب الرد على رسالة العضو الذي تريد تحذيره.")
    target_id = r.sender_id
    w = add_warning(str(target_id), str(chat_id))
    p = await r.get_sender()
    x = await ment(p)
    b = [Button.inline("الغاء التحذير", data=f"delwarn:{target_id}:{chat_id}"), Button.inline("تصفير التحذيرات", data=f"zerowarn:{target_id}:{chat_id}")]
    l = await link(event)
    await event.respond(
        f'تم تحذير المستخدم {x} ( `target_id` ) \n تحذيراته صارت ( 3/{w} )',
        buttons=b
    )
    restriction_duration = 900
    await event.delete()
    await r.delete()
    if w == 3 and await is_admin(chat_id, target_id):
        now = int(time.time())
        restriction_end_times.setdefault(event.chat_id, {})[target_id] = now + restriction_duration
    elif w == 3 and not await is_admin(chat_id, target_id):
        now = int(time.time())
        rights = ChatBannedRights(
            until_date=now + restriction_duration,
            send_messages=True)
        await ABH(EditBannedRequest(channel=chat_id, participant=target_id, banned_rights=rights))
        restriction_end_times.setdefault(event.chat_id, {})[target_id] = now + restriction_duration
        return
    await botuse("تحذير مستخدمين")
    if lc:
        s = await mention(event)
        await ABH.send_message(
            lc, 
            f"🚨 تم تحذير المستخدم:\n"
            f"👤 الاسم: {x}\n"
            f"🆔 الايدي: `{target_id}`\n"
            f"⚠️ عدد التحذيرات: {w} / 3"
            f"رابط الرسالة: {l}",
        )
        await try_forward(event, lc)
        return 
