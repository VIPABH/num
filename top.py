from ABH import ABH, events
import json
def load_points(filename="points.json"):
    try:
        with open(filename, "r") as file:
            return json.load(file)
    except FileNotFoundError:
        return {}
def save_points(data, filename="points.json"):
    with open(filename, "w") as file:
        json.dump(data, file, indent=4)
points = load_points()
def add_points(uid, gid, points_dict, amount=0):
    uid, gid = str(uid), str(gid)
    if uid not in points_dict:
        points_dict[uid] = {}
    if gid not in points_dict[uid]:
        points_dict[uid][gid] = {"points": 0}
    points_dict[uid][gid]["points"] += amount
    save_points(points_dict)
def add_user(uid, gid, name, rose, amount):
    uid, gid = str(uid), str(gid)
    if gid not in rose:
        rose[gid] = {}
    if uid not in rose[gid]:
        rose[gid][uid] = {
            "name": name,
            "status": "عادي",
            "giver": None,
            "m": amount,
            "promote_value": 0
        }
@ABH.on(events.NewMessage(pattern=r'^الاغنياء$'))
async def show_top_10_rich(event):
    gid=str(event.chat_id)
    if gid not in points:
        await event.reply("لا يوجد مشاركون في هذه المجموعة.")
        return
    all_users=[(uid,user_data[gid]["points"]) for uid,user_data in points.items() if gid in user_data]
    if not all_users:
        await event.reply("لا يوجد مشاركون في هذه المجموعة.")
        return
    top_users=sorted(all_users,key=lambda x:x[1],reverse=True)[:10]
    message="**🏅 أفضل 10 لاعبين في هذه المجموعة:**\n"
    for i,(uid,score) in enumerate(top_users,1):
        try:
            user=await ABH.get_entity(uid)
            name=user.first_name or "مستخدم"
            mention=f"[{name}](tg://user?id={uid})"
            message+=f"{i}. {mention} - `{score}` نقطة\n"
        except:continue
    await event.reply(message,parse_mode='md')
@ABH.on(events.NewMessage(pattern=r'^اضف فلوس (\d+)$'))
async def add_money(event):
    uid = event.sender_id
    r = await event.get_reply_message()
    if uid == 1910015590:
        p = int(event.pattern_match.group(1))
        gid = event.chat_id
        user_id = r.sender_id
        add_points(user_id, gid, points, amount=p)
        await event.reply(f"تم اضافة {p} دينار ل {r.sender.first_name}")
@ABH.on(events.NewMessage(pattern='ثروتي'))
async def m(event):
    uid = str(event.sender_id)
    gid = str(event.chat_id)
    if uid in points and gid in points[uid]:
        m = points[uid][gid]['points']
    else:
        m = 0
    await event.reply(f'فلوسك ↢ ( `{m}` )')
@ABH.on(events.NewMessage(pattern='ثروته|الثروه'))
async def replym(event):
    r = await event.get_reply_message()
    uid = str(r.sender_id)
    gid = str(event.chat_id)
    if uid in points and gid in points[uid]:
        m = points[uid][gid]['points']
    else:
        m = 0
    await event.reply(f'فلوسه ↢ ( `{m}` )')
@ABH.on(events.NewMessage(pattern=r'^حول (\d+(\.\d+)?)'))
async def send_money(event):
    reply = await event.get_reply_message()
    if not reply:
        await event.reply('عزيزي، لازم ترد على رسالة الشخص اللي تريد تحوّله.')
        return
    try:
        count = int(float(event.pattern_match.group(1)))
    except ValueError:
        await event.reply('تأكد من كتابة رقم صحيح بعد كلمة `حول`.')
        return
    if count <= 2999:
        await event.reply('المبلغ يجب أن يكون أكبر من 3000.')
        return
    user1_id = event.sender_id
    user2_id = reply.sender_id
    gid = str(event.chat_id)
    if str(user1_id) not in points or gid not in points[str(user1_id)]:
        await event.reply("ليس لديك نقاط كافية.")
        return
    if str(user2_id) not in points:
        points[str(user2_id)] = {}
    if gid not in points[str(user2_id)]:
        points[str(user2_id)][gid] = {"points": 0}
    sender_points = points[str(user1_id)][gid]["points"]
    if count > sender_points:
        await event.reply('رصيدك لا يكفي لهذا التحويل.')
        return
    points[str(user1_id)][gid]["points"] -= count
    points[str(user2_id)][gid]["points"] += count
    with open("points.json", "w", encoding="utf-8") as f:
        json.dump(points, f, ensure_ascii=False, indent=2)
    user1 = await ABH.get_entity(user1_id)
    user2 = await ABH.get_entity(user2_id)
    mention1 = f"[{user1.first_name}](tg://user?id={user1_id})"
    mention2 = f"[{user2.first_name}](tg://user?id={user2_id})"

    await event.reply(
        f"💸 تم التحويل بنجاح!\n\n"
        f"🔁 {mention1} ➡️ {mention2}\n"
        f"📦 المبلغ: `{count}` دينار"
    )
