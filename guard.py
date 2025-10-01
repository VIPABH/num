from telethon.tl.types import ChannelParticipantCreator, ChannelParticipantAdmin, ChatBannedRights
from telethon.tl.functions.channels import EditBannedRequest, GetParticipantRequest
from telethon.tl.types import ChatBannedRights, MessageEntityUrl
from telethon.errors import UserNotParticipantError
from Program import r as redas, chs
from other import botuse, is_owner
from telethon import events, Button
from top import points, delpoints
import asyncio, re, json, time
from Resources import *
from ABH import ABH
@ABH.on(events.NewMessage(pattern=r"^الغاء تقييد عام(?:\s+(.*))?$"))
async def delrestrict(e):
    id = e.sender_id
    a = await is_owner(e.chat_id, id)
    z = await can_ban_users(e.chat_id, id)
    s = save(None, "secondary_devs.json")
    k = str(e.chat_id) in s and str(id) in s[str(e.chat_id)]
    if not (
        a
        or z
        or k
    ):
        await chs(e, "ليس لديك صلاحيات كافية.")
        return
    # r = await e.get_reply_message()
    target =await to(e)
    await hint(f"{target}")
    if target:
    # if not r or not r.sender_id:
        await chs(e, "الرجاء الرد على رسالة المستخدم المراد إلغاء تقييده.")
        return    
    m = await ment(r)
    if not delres(chat_id=e.chat_id, user_id=r.sender_id):
        await chs(e, "هذا المستخدم ليس مقيداً حالياً.")
        return
    participant = await ABH(GetParticipantRequest(channel=int(e.chat_id), participant=int(r.sender_id)))
    if isinstance(participant.participant, (ChannelParticipantAdmin)):
        await chs(e, f"تم إلغاء كتم المشرف ( {m} ).")
        await send(e, f'#الغاء_تقييد_عام\n تم الغاء تقييد المشرف \n اسمه: ( {m} ) \n🆔 ايديه: `{r.sender_id}`\n👤 بواسطة المعاون \n اسمه: ( {await mention(e)} ) \n ايديه: ( `{e.sender_id}` )')
        return
    else:
        rights = ChatBannedRights(
            until_date=None,
            send_messages=False
        )
        try:
            await ABH(EditBannedRequest(channel=int(e.chat_id), participant=int(r.sender_id), banned_rights=rights))
        except Exception as ex:
            await chs(e, "لا يمكنني إلغاء تقييد هذا المستخدم.")
            await hint(ex)
            return
    await send(e, f'#الغاء_تقييد_عام\n تم الغاء تقييد المستخدم \n اسمه: ( {m} ) \n🆔 ايديه: `{r.sender_id}`\n👤 بواسطة المعاون \n اسمه: ( {await mention(e)} ) \n ايديه: ( `{e.sender_id}` )')
    await botuse("الغاء تقييد عام")
    await chs(e, f"المستخدم ( {m} ) تم إلغاء تقييده.")
@ABH.on(events.NewMessage(pattern=r"^المقيدين عام$"))
async def list_restricted(event):
    chat_id = str(event.chat_id)
    now = int(time.time())
    all_data = await res(None)
    if chat_id not in all_data or not all_data[chat_id]:
        await event.reply("لا يوجد حالياً أي مستخدم مقيد.")
        return
    msg = "📋 قائمة المقيدين عام:\n\n"
    for user_id, end_time in list(all_data[chat_id].items()):
        remaining = end_time - now
        if remaining <= 0:
            delres(chat_id=chat_id, user_id=user_id)
            continue
        try:
            user = await ABH.get_entity(int(user_id))
            name = f"[{user.first_name}](tg://user?id={user_id})"
            minutes, seconds = divmod(int(remaining), 60)
            msg += f"● {name} ↔ `{user_id}`\n⏱️ باقي: {minutes} دقيقة و {seconds} ثانية\n\n"
        except Exception as e:
            msg += f"مستخدم غير معروف — `{user_id}`\n"
            await hint(e)
    if msg.strip() == "📋 قائمة المقيدين عام:":
        msg = "لا يوجد حالياً أي مستخدم مقيد."
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
    restriction_duration = 60
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
    await send(event, f"تم تقييد المستخدم {target_name} بواسطة {sender_name} تقييد ميم مدة 60 ث")
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
    chat_id = event.chat_id
    user_id = event.sender_id
    text = event.text
    if not is_assistant(str(chat_id), user_id) or text == "تقييد ميم":
        await notAssistantres(event)
        # await chs(event, 'شني خالي كبينه انت مو معاون')
        return
    r = await event.get_reply_message()
    if not r:
        return await event.reply("يجب الرد على رسالة العضو الذي تريد تقييده.")
    name = await ment(r)
    try:
        participant = await ABH(GetParticipantRequest(channel=int(chat_id), participant=int(r.sender_id)))
        if isinstance(participant.participant, (ChannelParticipantCreator, ChannelParticipantAdmin)):
            await try_forward(r)
            await r.delete()
            await event.delete()
            await res(event)
            await send(event, f'#تقييد_عام\n تم كتم المشرف \n اسمه: ( {name} ) \n🆔 ايديه: `{r.sender_id}`\n👤 بواسطة المعاون \n اسمه: ( {await mention(event)} ) \n ايديه: ( `{event.sender_id}` )')
            await chs(event, f'تم كتم {name} مدة 20 دقيقه')
            return
    except Exception as ex:
        await hint(ex)
        return
    now = int(time.time())
    rights = ChatBannedRights(
        until_date=now + 20 * 60,
        send_messages=True
    )
    await res(event)
    try:
        await ABH(EditBannedRequest(channel=int(chat_id), participant=int(r.sender_id), banned_rights=rights))
        type = "تقييد عام"
        await botuse(type)
        ء = await r.get_sender()
        rrr = await ment(ء)
        c = f"تم تقييد {rrr} لمدة 20 دقيقة."
        await ABH.send_file(event.chat_id, "https://t.me/VIPABH/592", caption=c)
        await send(event, f'#تقييد_عام\n تم تقييد المستخدم \n اسمه: ( {rrr} ) \n🆔 ايديه: `{r.sender_id}`\n👤 بواسطة المعاون \n اسمه: ( {await mention(event)} ) \n ايديه: ( `{event.sender_id}` )')
        await try_forward(r)
        await r.delete()
        await event.delete()
    except Exception as ex:
        await hint(ex)
        await event.reply(f" قيدته بس ماكدرت امسح الرساله ")
@ABH.on(events.NewMessage)
async def monitor_messages(event):
    if not event.is_group:
        return
    user_id = event.sender_id
    chat_id = event.chat_id
    now = int(time.time())
    all_data = await res(None)
    if str(chat_id) in all_data and str(user_id) in all_data[str(chat_id)]:
        end_time = all_data[str(chat_id)][str(user_id)]
        remaining = end_time - now
        if remaining <= 0:
            del all_data[str(chat_id)][str(user_id)]
            if not all_data[str(chat_id)]:
                del all_data[str(chat_id)]
            with open('res.json', 'w', encoding='utf-8') as f:
                json.dump(all_data, f, ensure_ascii=False, indent=4)
                return
        participant = await ABH(GetParticipantRequest(channel=int(chat_id), participant=int(user_id)))
        if isinstance(participant.participant, (ChannelParticipantCreator, ChannelParticipantAdmin)):
            await event.delete()
            return
        rights = ChatBannedRights(
            until_date=now + remaining,
            send_messages=True
        )
        await ABH(EditBannedRequest(
            channel=int(chat_id),
            participant=int(user_id),
            banned_rights=rights
        ))
        rrr = await mention(event)
        c = f"تم اعاده تقييد {rrr} لمدة ** {remaining//60} دقيقة و {remaining%60} ثانية.**"
        await ABH.send_file(event.chat_id, "https://t.me/recoursec/15", caption=c)
        await send(event, f"#تقييد_عام \n تم اعادة تقييد {rrr} باقي على انتهاء وقت التقييد ** {remaining//60} دقيقة و {remaining%60} ثانية.** ")
        type = "تقييد مستخدمين"
        await botuse(type)
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
    try:
        perms = await ABH.get_permissions(chat_id, uid)
        if perms.is_admin:
            return
    except UserNotParticipantError:
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
    sent_msg = await ABH.send_message(
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
    report_data[sent_msg.id] = (uid, رابط, mention_text, date_posted, date_edited)
    await asyncio.sleep(60)
    if uid in whitelist:
        await sent_msg.delete()
        return
@ABH.on(events.CallbackQuery(pattern=r'^yes:(\d+)$'))
async def yes_callback(event):
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
@ABH.on(events.CallbackQuery(pattern=r'^no:(\d+)$'))
async def no_callback(event):
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
    "بكسختك", "🍑", "نغل", "نغولة", "نغوله", "ينغل", "كس", "عير", "كسمك", "كسختك", "خرب ابربك", 
    "اتنيج", "ينيج", "طيرك", "ارقه جاي", "يموط", "تموط", "موطلي", "اموط", "بورن", 'زبري', 'بزبري',
    "كس امك", "طيز", "طيزك", "فرخ", "كواد", "اخلكحبة", "اينيج", "بربوك", "زب", "انيجمك", "الكواد",
    "فريخ", "فريخة", "فريخه", "فرخي", "قضيب", "مايا", "ماية", "مايه", "بكسمك", "تيل بيك", "كومبي",
    "الفرخ", "تيز", "كسم", "سكسي", "كحاب", "مناويج", "منيوج", "عيورة","انزع", "انزعي", "خرب الله",
    "احط رجلي", "عاهرات", "عواهر", "عاهره", "عاهرة", "ناكك", "اشتعل دينه", "احترك دينك", "الجبة",
    "تيز", "التيز", "الديوث", "كسمج", "بلبولك", "صدرج", "كسعرضك" , "الخنيث", "انزعو", "انزعوا",
    "طيزها", "عيري", "خرب الله", "العير", "بعيري", "كحبه", "برابيك", "نيجني", "العريض", "الجبه",
    "خرب بربك", "خربربج", "خربربها", "خرب بربها", "خرب بربة", "خرب بربكم", "كومبي", "مدودة",
    "كمبي", "كوم بي", "قوم بي", "قم بي", "قوم به", "كومت", "قومت", "الطيازه", "دوده", 'دودة',
    "نيچني", "نودز", "نتلاوط", "لواط", "لوطي", "فروخ", "منيوك", "خربدينه", "خربدينك", "مدود",
    "ارقة جاي", "انيجك", "نيجك", "كحبة", "ابن الكحبة", "ابن الكحبه", "تنيج", "كسين", "مدوده",
    "عيورتكم", "انيجة", "انيچة", "انيجه", "انيچه", "أناج", "اناج", "انيج", "أنيج", "منيوك",
    "خرب دينه", "كسك", "كسه", "كسة", "اكحاب", "أكحاب", "زنا", "كوم بي", "كمبي", 
    "خربدينة", "خربدينج", "خربدينكم", "خربدينها", "خربربه", "خربربة", "خربربك", 
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
        'ـ': '',
        'ض': '',
        '/': '',
        '\\': '',
        '|': '',
        '.': '',
        ',': '',
        '’': '',
        '_': '',
        '-': '',
        '$': '',
        'ال': '',
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
@ABH.on(events.NewMessage)
async def handler_res(event):
    message_text = event.raw_text
    user_id = event.sender_id
    chat = event.chat_id
    now = int(time.time())
    lock_key = f"lock:{event.chat_id}:تقييد"
    x = redas.get(lock_key) == "True"
    if not event.is_group or not event.raw_text or not x:
        return
    x = contains_banned_word(message_text)
    b = [Button.inline(f'الغاء التحذير', data=f'delwarn:{chat}:{user_id}'), Button.inline('تصفير التحذيرات', data=f'zerowarn:{chat}:{user_id}')]
    الغاء = Button.inline('الغاء التقييد', data=f'unres:{chat}|{user_id}')
    xx = await event.get_sender()
    ء = await ment(xx)
    l = await link(event)
    if not x:
        return
    await botuse('تحذير بسبب الفشار')
    assis = is_assistant(chat, user_id)
    if assis:
        await send(
            event,
            f"⚠️ تم رصد مخالفة:\n"
            f"👤 #المعاون: {ء}\n"
            f"🆔 الآيدي: `{user_id}`\n"
            f"📝 الكلمة الممنوعة: `{x}`\n"
            f"🔗 الرابط: {l}"
        )
        await try_forward(event)
        await event.delete()
        return
    w = add_warning(user_id, chat)
    now = int(time.time())
    restriction_duration = 600
    if w == 3:
        if await is_admin(chat, user_id):
            restriction_end_times.setdefault(event.chat_id, {})[user_id] = now + restriction_duration
            await event.respond(
                f"🔇 تم كتم المشرف {ء}\n🆔 الايدي: `{user_id}`\n📑 السبب: تكرار إرسال الكلمات المحظورة.",
                buttons=الغاء
                )
            await try_forward(event)       
            await send(
                event,
                f"🔇 تم كتم #المشرف:\n👤 {ء} │ 🆔 `{user_id}`\n📑 السبب: كثرة المخالفات\n✉️ أرسل: {x}\n🔗 الرابط: {l}",
            )
            await try_forward(event)
            await event.delete()
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
            await try_forward(event)
            await event.delete()
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
    await try_forward(event)
    await event.delete()
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
    if is_assistant(chat_id, target_id) and is_assistant(chat_id, user_id):
        await chs(event, 'غراب يكول لغراب وجهك اسود')
        return
    if is_assistant(chat_id, target_id):
        await chs(event, 'هييييييه متكدر تحذر المعاون')
        return
    w = add_warning(str(target_id), str(chat_id))
    p = await r.get_sender()
    x = await ment(p)
    b = [Button.inline("الغاء التحذير", data=f"delwarn:{target_id}:{chat_id}"), Button.inline("تصفير التحذيرات", data=f"zerowarn:{target_id}:{chat_id}")]
    l = await link(event)
    await event.respond(
        f'تم تحذير المستخدم {x} ( `{target_id}` ) \n تحذيراته صارت ( 3/{w} )',
        buttons=b
    )
    restriction_duration = 900
    await try_forward(r)
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
    المحذر= await mention(event)
    await send(
        event, 
        f"🚨 ┇ #تـحـذيـر ┇ 🚨\n"
        f"👤 المُحَذِّر:   {المحذر}\n"
        f"👤 المُحَذَّر:   {x}\n"
        f"🆔 الآيـدي:   `{target_id}`\n"
        f"⚠️ التحذيرات:   {w} / 3\n"
        f"🔗 رابط الرسالة:   {l}"
    )
    await try_forward(event)
    await event.delete()
@ABH.on(events.CallbackQuery)
async def warnssit(e):
    data = e.data.decode('utf-8') if isinstance(e.data, bytes) else e.data
    parts = data.split(':')
    if len(parts) == 3:
        if not is_assistant(e.chat_id, e.sender_id):
            return await e.answer('🌚')
        النوع, target_id, chat_id = parts
        msg = await e.get_message()
        t = msg.text
        if النوع == "zerowarn":
            await e.edit(f"{t} \n ```تم تصفير التحذيرات```")
            zerowarn(target_id, chat_id)
        elif النوع == 'delwarn':
            d = del_warning(target_id, chat_id)
            m = await mention(e)
            await e.edit(f"تم تعديل التحذيرات بواسطه {m} \n التحذيرات صارت {d}")
@ABH.on(events.NewMessage(pattern=r'^(تحذيراتي|تحذيرات(ه|ة))$'))
async def showwarns(e):
    t = e.text
    chat = e.chat_id
    target_id = None
    if t == 'تحذيراتي':
        target_id = e.sender_id
    else:
        r = await e.get_reply_message()
        if not r:
            await chs(e, "⚠️ لازم ترد على رسالة الشخص")
            return
        target_id = r.sender_id
    معاون = is_assistant(chat, target_id)
    if معاون:
        await chs(e, "لك شمعة ماكو تحذيرات")
        return
    w = count_warnings(int(target_id), int(chat))
    await chs(e, f' ( 3/{w} )')
@ABH.on(events.NewMessage(pattern="!تجربة"))
async def test(e):
    t = await auth(e)
    await e.reply(f"{t}")
