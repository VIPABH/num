from telethon.tl.types import ChannelParticipantAdmin, ChannelParticipantCreator, ChatAdminRights
from telethon.tl.functions.channels import GetParticipantRequest, EditAdminRequest
from top import points, save_points#type: ignore
from other import * #type: ignore
from Program import chs #type: ignore
from telethon import events, Button
from ABH import ABH #type: ignore
from guard import is_admin
from Resources import *
@ABH.on(events.NewMessage(pattern=r"^(تغيير لقبي|تغيير لقب(?:ه|ها|ة))\s*(.*)$"))
async def change_own_rank(event):
    user_id = event.sender_id
    if not event.is_group:
        return
    chat = await event.get_chat()
    me = await ABH.get_permissions(chat.id, 'me')
    if not me.is_admin or not me.add_admins:
        await chs(event, " لا أمتلك صلاحية تعديل المشرفين.")
        await react(event, "💔")
        return
    r = await event.get_reply_message()
    if event.text.startswith("تغيير لقبي"):
        user_id = event.sender_id
    else:
        if not r:
            await react(event, "🤔")
            await chs(event, "سوي رد على مشرف حتى اغيرلك لقبه")
            return
        user_id = r.sender_id
    x = await auth(event)
    if (not x or x == "المعاون") and not event.text.startswith("تغيير لقبي"):
        await chs(event, "هذا الامر يخص المطور الاساسي والمطورين الثانويين فقط")
        return
    new_rank = event.pattern_match.group(2)
    if not new_rank:
        await react(event, "🤔")
        await chs(event, "اكتب اللقب وي الامر ك `تغيير لقبي ` + لقب.")
        return
    await botuse("تغيير لقبي")
    o = await get_owner(event)
    if user_id == o.id:
        await react(event, "🤣")
        await event.reply('هاي عود انت المالك')
        return
    x = await ABH.get_me()
    result = await ABH(GetParticipantRequest(channel=chat.id, participant=user_id))
    if isinstance(result.participant, ChannelParticipantAdmin):
        if result.participant.promoted_by != x.id:
            user = await ABH.get_entity(result.participant.promoted_by)
            menti = await ment(user)
            await chs(event, f"خلي {menti} يعدل اللقب لدوخني توكل")
            await react(event, "🤣")
            return
    if len(new_rank) > 14:
        await chs(event, "اللقب لازم يكون اقل من 14 حرف.")
        await react(event, "👍")
        return
    try:
        pp = await ABH(GetParticipantRequest(chat.id, user_id))
        participant = pp.participant
    except Exception as e:
        await ABH.send_message(wfffp, f"خطأ في جلب بيانات المستخدم: {e}")
        await event.reply(f"والله مابيه حيل اعذرني يخوي")
        await react(event, "💔")
        return
    if not isinstance(participant, (ChannelParticipantAdmin, ChannelParticipantCreator)):
        await chs(event, "يالفقير لازم يكون مشرف بالاول علمود اغيرلك لقب🙄🙄.")
        await react(event, "🤣")
        return
    admin_right = participant.admin_rights
    try:
        await ABH(EditAdminRequest(
            channel=chat.id,
            user_id=user_id,
            admin_rights=admin_right,
            rank=new_rank
        ))
        await chs(event, f"تم تغيير اللقب الى `{new_rank}`")
        await react(event, "👍")
    except Exception as e:
        await ABH.send_message(wfffp, f"خطأ عند تعديل اللقب: {e}")
        await chs(event, "والله مابيه حيل اعذرني يخوي")
        await react(event, "💔")
promot = {}
session = {}
@ABH.on(events.NewMessage(pattern='^ترقية$'))
async def promoteADMIN(event):
    if not event.is_group:
        return
    chat = await event.get_chat()
    user_id = event.sender_id
    me = await ABH.get_permissions(chat.id, 'me')
    if not me.is_admin or not me.add_admins:
        await chs(event, " لا أمتلك صلاحية تعديل المشرفين.")
        await react(event, "💔")
        return
    type = "ترقية"
    await botuse(type)
    isc = await can_add_admins(chat, user_id)
    sm = await mention(event)
    x = await auth(event)
    if not x or x == "المعاون":
        await chs(event, f"عذرًا ( {sm} )، هذا الأمر مخصص للمالك فقط.")
        await react(event, "💔")
        return
    r = await event.get_reply_message()
    if not r:
        await chs(event, 'لازم تسوي رد لشخص علمود ارفعه')
        await react(event, "🤔")
        return
    chat_id = event.chat_id
    if chat_id not in promot:
        promot[chat_id] = {}
    if chat_id not in session:
        session[chat_id] = {}
    session[chat_id].update({'pid': user_id, 'top': r.sender_id})
    target_user_id = r.sender_id
    promot[chat_id][target_user_id] = {
        'rights': {
            'change_info': False,
            'delete_messages': False,
            'ban_users': False,
            'invite_users': False,
            'pin_messages': False,
            'add_admins': False,
            'manage_call': False,
        },
    }
    isp = await is_admin(chat, target_user_id)
    if isp:
        await react(event, "🤔")
        c = 'المستخدم مشرف ومرفوع من قبل'
        await ABH.send_file(
            entity=event.chat_id,
            file='https://t.me/recoursec/16',
            caption=c,
            reply_to=event.id
        )
        return
    buttons = [
        [Button.inline('تغيير معلومات', data='change_info'), Button.inline('حذف رسائل', data='delete_messages')],
        [Button.inline('حظر المستخدمين', data='ban_users'), Button.inline('دعوة', data='invite_users')],
        [Button.inline('الاتصال', data='manage_call'), Button.inline('اضافة مشرفين', data='add_admins')],
        [Button.inline('تثبيت رسائل', data='pin_messages')],
        [Button.inline('تم', data='done')]
        ]
    c = 'يتم رفع المستخدم مشرف \n يرجى تحديد الصلاحيات'
    await ABH.send_file(
        entity=event.chat_id,
        file='https://t.me/VIPABH/1219',
        caption=c,
        reply_to=event.id,
        buttons=buttons)
async def promoti(event):
    data = event.data.decode('utf-8')
    chat_id = event.chat_id
    if chat_id in session:
        initiator_id = session[chat_id]['pid']
        target_user_id = session[chat_id]['top']
        if event.sender_id != initiator_id:
            await event.answer('ما تكدر تعدل شيء هنا', alert=True)
            return
        if chat_id in promot and target_user_id in promot[chat_id]:
            rights = promot[chat_id][target_user_id]['rights']
            if data == 'done':
                await event.answer('تم تنفيذ الترقية', alert=False)
                await event.edit('تم رفع المستخدم بنجاح \n لتغيير اللقب ارسل ```تغيير لقبي ``` + لقب معين ')
                admin_rights = ChatAdminRights(
                    change_info=rights.get('change_info', False),
                    delete_messages=rights.get('delete_messages', False),
                    ban_users=rights.get('ban_users', False),
                    invite_users=rights.get('invite_users', False),
                    pin_messages=rights.get('pin_messages', False),
                    add_admins=rights.get('add_admins', False),
                    manage_call=rights.get('manage_call', False),
                    manage_topics=False,
                    anonymous=False,
                    post_stories=True,
                    edit_stories=True,
                    delete_stories=True
                )
                c = f'BY {bot}'
                await ABH(EditAdminRequest(event.chat_id, target_user_id, admin_rights, rank=c))
                del session[chat_id]
                del promot[chat_id][target_user_id]
                return
            current_value = rights.get(data, False)
            new_value = not current_value
            rights[data] = new_value
            status = "مفعلة 👍" if new_value else "ملغية ❌"
            await event.answer(f"تم تعديل صلاحية: {data} → {status}", alert=False)
            buttons = [
                [Button.inline(f"تغيير المعلومات {'👍' if rights.get('change_info') else '❌'}", b'change_info')],
                [Button.inline(f"حذف الرسائل {'👍' if rights.get('delete_messages') else '❌'}", b'delete_messages')],
                [Button.inline(f"حظر المستخدمين {'👍' if rights.get('ban_users') else '❌'}", b'ban_users')],
                [Button.inline(f"دعوة مستخدمين {'👍' if rights.get('invite_users') else '❌'}", b'invite_users')],
                [Button.inline(f"تثبيت الرسائل {'👍' if rights.get('pin_messages') else '❌'}", b'pin_messages')],
                [Button.inline(f"إضافة مشرفين {'👍' if rights.get('add_admins') else '❌'}", b'add_admins')],
                [Button.inline(f"إدارة المكالمات {'👍' if rights.get('manage_call') else '❌'}", b'manage_call')],
                [Button.inline("✅ تنفيذ", b'done')]
            ]
            await event.edit("اختر الصلاحيات:", buttons=buttons)
async def dodemote(event, target_user_id=None):
    chat_id = event.chat_id
    if not event.is_group:
        return
    if target_user_id is None:
        target_user_id = event.sender_id
    me = await ABH.get_permissions(chat_id, 'me')
    if not me.is_admin or not me.add_admins:
        await chs(event, " لا أمتلك صلاحية تعديل المشرفين.")
        await react(event, "💔")
        return False
    try:
        pp = await ABH(GetParticipantRequest(int(chat_id), int(target_user_id)))
        participant = pp.participant
    except Exception as e:
        await ABH.send_message(wfffp, f"خطأ في جلب بيانات المستخدم: {e}")
        await event.reply("والله مابيه حيل اعذرني يخوي")
        await react(event, "💔")
        return False
    x = await ABH.get_me()
    if hasattr(participant, "promoted_by") and participant.promoted_by != x.id:
        user = await ABH.get_entity(participant.promoted_by)
        menti = await ment(user)
        await chs(event, f"خلي {menti} ينزله من المشرفين، مو شغلي 😅")
        await react(event, "🤣")
        return False
    try:
        await ABH(EditAdminRequest(
            channel=int(chat_id),
            user_id=int(target_user_id),
            admin_rights=ChatAdminRights(
                change_info=False,
                post_messages=False,
                edit_messages=False,
                delete_messages=False,
                ban_users=False,
                invite_users=False,
                pin_messages=False,
                add_admins=False,
                manage_call=False,
                manage_topics=False,
                anonymous=False,
                post_stories=False,
                edit_stories=False,
                delete_stories=False
            ),
            rank=''
        ))
        await react(event, "👍")
        return True
    except Exception as e:
        await ABH.send_message(wfffp, f"خطأ عند تنزيل المشرف: {e}")
        await chs(event, "والله مابيه حيل اعذرني يخوي")
        await react(event, "💔")
        return False
@ABH.on(events.NewMessage(pattern='^مخفي نزلني|تنزيل مشرف|مخفي نزل(ه|ة)$'))
async def demote_admin(event):
    if not event.is_group:
        return
    if event.text == "مخفي نزلني":
        done = await dodemote(event)
        if done:
        return await chs(e, "تم تنزيلك من المشرفين")
    r = await event.get_reply_message()
    if not r:
        await chs(event, 'لازم تسوي رد لشخص علمود انزله من المشرفين')
        await react(event, "🤔")
        return
    chat_id = event.chat_id
    target_user_id = r.sender_id
    a = await auth(event)
    if not a or a == "المعاون":
        await chs(event, 'الامر يخص المالك فقط وبعض المشرفين')
        await react(event, "💔")
        return
    try:
        pp = await ABH(GetParticipantRequest(chat_id, target_user_id))
        participant = pp.participant
    except Exception as e:
        await ABH.send_message(wfffp, f"خطأ في جلب بيانات المستخدم: {e}")
        await event.reply("والله مابيه حيل اعذرني يخوي")
        await react(event, "💔")
        return
    if not isinstance(participant, (ChannelParticipantAdmin, ChannelParticipantCreator)):
        await chs(event, "المستخدم مو مشرف اصلاً.")
        await react(event, "🤣")
        return
    if isinstance(participant, ChannelParticipantCreator):
        await chs(event, "ما اكدر انزله لان هو المالك.")
        await react(event, "🤣")
        return
    ء = await dodemote(event, target_user_id)
    if ء:
        await chs(event, "تم التنزيل ب نجاح.")
        return
