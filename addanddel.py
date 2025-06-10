from telethon.tl.types import ChannelParticipantsAdmins, ChannelParticipantCreator
from telethon.tl.functions.channels import GetParticipantsRequest
from telethon.tl.functions.channels import GetParticipantRequest
from telethon.tl.functions.channels import EditAdminRequest
from telethon.tl.types import ChannelParticipantAdmin
from telethon.tl.types import ChatAdminRights
from top import points, add_user, save_points
from telethon import events
from other import botuse
from ABH import ABH
async def get_owner(event):
    if not event.is_group:
        return None   
    chat = await event.get_chat()
    if getattr(chat, 'megagroup', False):
        try:
            result = await ABH(GetParticipantsRequest(
                channel=chat,
                filter=ChannelParticipantsAdmins(),
                offset=0,
                limit=100,
                hash=0
            ))
            for participant in result.participants:
                if isinstance(participant, ChannelParticipantCreator):
                    user = await ABH.get_entity(participant.user_id)
                    return user
        except:
            return None
    return None
async def can_add_admins(event):
    if not event.is_group:
        return False
    try:
        chat = await event.get_chat()
        user_id = event.sender_id
        result = await ABH(GetParticipantRequest(
            channel=chat,
            participant=user_id
        ))
        role = result.participant
        if isinstance(role, ChannelParticipantCreator):
            return True
        if isinstance(role, ChannelParticipantAdmin):
            rights = role.admin_rights
            if rights and rights.add_admins:
                return True
        return False
    except Exception as e:
        print(f"خطأ في can_add_admins: {e}")
        return False
@ABH.on(events.NewMessage(pattern='^رفع مشرف$'))
async def promoteADMIN(event):
    o = await get_owner(event)
    isc = await can_add_admins(event)
    uid = event.sender_id
    if uid != o.id and uid != 1910015590 and not isc:
        await event.reply('الامر يخص المالك فقط وبعض المشرفين')
        return
    await event.reply('يجري رفع المستخدم مشرف')
@ABH.on(events.NewMessage(pattern=r'رفع سمب(?:\s+(\d+))?'))
async def promote_handler(event):
    type = "رفع سمب"
    await botuse(type)
    message = await event.get_reply_message()
    if not message or not message.sender:
        await event.reply("يجب الرد على شخص حتى ترفعه.")
        return
    match = event.pattern_match
    amount = int(match.group(1)) if match.group(1) else 1001
    uid = str(event.sender_id)
    target_id = str(message.sender_id)
    giver_name = (await event.get_sender()).first_name or "مجهول"
    if target_id == 1910015590:
        await event.reply(f'جاري رفع {giver_name} سمب')
    receiver_name = message.sender.first_name or "مجهول"
    gid = str(event.chat_id)
    add_user(target_id, gid, receiver_name, points, 0)
    add_user(uid, gid, giver_name, points, 0)
    if points[gid][target_id].get("status") == "مرفوع":
        await event.reply(f"{receiver_name} مرفوع من قبل.")
        return
    if amount < 1000:
        await event.reply("أقل مبلغ مسموح للرفع هو 1000.")
        return
    giver_money = points[uid][gid]['points']
    if giver_money < 1000:
        await event.reply(f" رصيدك {giver_money}، والحد الأدنى للرفع هو 10.")
        return
    if giver_money < amount:
        await event.reply(f" رصيدك لا يكفي. تحاول ترفع بـ {amount} فلوس ورصيدك فقط {giver_money}.")
        return
    points[uid][gid]['points'] = giver_money - amount
    points[gid][target_id]["status"] = "مرفوع"
    points[gid][target_id]["giver"] = uid
    points[gid][target_id]["promote_value"] = amount
    save_points(points)
    await event.reply(f" تم رفع {receiver_name} مقابل {amount} فلوس")
@ABH.on(events.NewMessage(pattern='تنزيل سمب'))
async def demote_handler(event):
    type = "تنزيل سمب"
    await botuse(type)
    message = await event.get_reply_message()
    if not message or not message.sender:
        await event.reply("متكدر تنزل العدم , سوي رد على شخص")
        return
    gid = str(event.chat_id)
    sender_id = str(event.sender_id)
    target_id = str(message.sender_id)
    target_name = message.sender.first_name or "مجهول"
    add_user(target_id, gid, target_name, points, 0)
    add_user(sender_id, gid, event.sender.first_name, points, 0)
    if points[gid].get(target_id, {}).get("status") != "مرفوع":
        await event.reply("المستخدم هاذ ما مرفوع من قبل😐")
        return
    giver_id = points[gid][target_id].get("giver")
    executor_money = points[sender_id][gid]['points']
    promote_value = points[gid][target_id].get("promote_value", 313)
    amount = int(promote_value * (1.5 if sender_id == giver_id else 2))
    if executor_money < amount:
        await event.reply(f"ما تگدر تنزله لأن رصيدك {executor_money}، والكلفة المطلوبة {amount}")
        return
    points[sender_id][gid]['points'] -= amount
    del points[gid][target_id]
    if not points[gid]:
        del points[gid]
    save_points(points)
    r = await event.get_reply_message()
    await event.reply(f"تم تنزيل {r.sender.first_name}  من السمبية")
@ABH.on(events.NewMessage(pattern='السمبات'))
async def show_handler(event):
    type = "السمبات"
    await botuse(type)
    chat_id = str(event.chat_id)
    if chat_id not in points or not points[chat_id]:
        await event.reply("ماكو سمبات هنا بالمجموعة")
        return
    response = "قائمة السمبات👇\n"
    removed_users = []
    for uid in list(points[chat_id].keys()):
        data = points[chat_id][uid]
        if data.get("status") == "مرفوع":
            status_icon = "👌"
            response += f"{status_icon} [{data['name']}](tg://user?id={uid}) ⇜ {data.get('promote_value', 0)}\n"
        else:
            removed_users.append(uid)
    for uid in removed_users:
        if points[chat_id].get(uid) and points[chat_id][uid].get("status") != "مرفوع":
            del points[chat_id][uid]
    save_points(points)
    await event.reply(response if response.strip() != "قائمة السمبات👇" else "ماكو وردات مرفوعين بالمجموعة", parse_mode="Markdown")
@ABH.on(events.NewMessage(pattern='اوامر الرفع'))
async def promot_list(event):
    type = "اوامر الرفع"
    await botuse(type)
    await event.reply('**اوامر الرفع كالاتي** \n `رفع سمب` + عدد فلوس \n لرفع الشخص في قائمة `السمبات` \n `تنزيل سمب` \n حتى ترفع لازم يكون رصيدك 1000 والتنزيل يُضرب المبلغ *1.5 \n * `اوامر الالعاب`')
