from ABH import ABH, events
from Resources import hint
from other import botuse
import json
wfffp = 1910015590
lit = [6498922948, 7176263278, 6520830528, 49820009, 1910015590]
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
def add_points(uid, gid, points, amount=0):
    try:
        uid = str(uid)
        if uid not in points:
            points[uid] = 0
        points[uid] += amount
        save_points(points)
    except Exception as e:
        print(e)
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
def delpoints(uid, gid, points, amount):
    uid, gid = str(uid), str(gid)
    if uid not in points:
        points[uid] = {}
    if gid not in points[uid]:
        points[uid][gid] = {"points": 0}
    points[uid][gid]["points"] = max(0, points[uid][gid]["points"] - amount)
    save_points(points)
@ABH.on(events.NewMessage(pattern='^الاغنياء$'))
async def show_rich(event):
    if not points:
        await event.reply("لا توجد بيانات ثروة حالياً.")
        return
    sorted_points = sorted(points.items(), key=lambda x: x[1], reverse=True)
    top_rich = sorted_points[:10]
    message = "أغنى الأشخاص:\n\n"
    for i, (uid, amt) in enumerate(top_rich, start=1):
        try:
            user = await event.client.get_entity(int(uid))
            name = user.first_name if user.first_name else "بدون اسم"
        except:
            name = f"مستخدم {uid}"
        message += f"{i}. {name} → `{amt}`\n"
    await event.reply(message)
@ABH.on(events.NewMessage(pattern=r'^اضف فلوس (\d+)$'))
async def add_money(event):
    if not event.is_group:
        return
    type = "اضف فلوس"
    await botuse(type)
    uid = event.sender_id
    r = await event.get_reply_message()
    if r.sender_id in lit and not uid != wfffp: 
        await event.reply("هههههه")
        return
    if uid in lit:
        p = int(event.pattern_match.group(1))
        gid = event.chat_id
        user_id = r.sender_id
        add_points(user_id, gid, points, amount=p)
        await event.reply(f"تم اضافة {p} دينار ل {r.sender.first_name}")
@ABH.on(events.NewMessage(pattern=r'^حذف فلوس (\d+)$'))
async def add_money(event):
    if not event.is_group:
        return
    type = "حذف فلوس"
    await botuse(type)
    uid = event.sender_id
    r = await event.get_reply_message()
    if r.sender_id in lit and uid != wfffp: 
        await event.reply("هههههه")
        return
    if uid in lit:
        p = int(event.pattern_match.group(1))
        gid = event.chat_id
        user_id = r.sender_id
        delpoints(user_id, gid, points, amount=p)
        await event.reply(f"تم حذف {p} دينار ل {r.sender.first_name}")
@ABH.on(events.NewMessage(pattern=r'^تصفير$'))
async def add_money(event):
    if not event.is_group:
        return
    type = "تصفير"
    await botuse(type)
    id = event.sender_id
    r = await event.get_reply_message()
    if r.sender_id in lit: 
        await event.reply("هههههه")
        return
    gid = event.chat_id
    if not r:
        await event.reply("يجب الرد على رسالة المستخدم الذي تريد تصفير نقاطه.")
        return
    uid = str(r.sender_id)
    gid = str(event.chat_id)
    if uid in points and gid in points[uid]:
        p = points[uid][gid].get('points', 0)
    delpoints(str(uid), str(gid), points, amount=int(p))
    await event.reply(f"تم حذف {p} دينار لـ {r.sender.first_name}")
@ABH.on(events.NewMessage(pattern='ثروتي'))
async def m(event):
    if not event.is_group:
        return
    type = "ثروتي"
    await botuse(type)
    uid = str(event.sender_id)
    gid = str(event.chat_id)
    if uid in points:
        m = points[uid]
    else:
        m = 0
    await event.reply(f'فلوسك ↢ ( `{m}` )')
@ABH.on(events.NewMessage(pattern='ثروته|الثروه'))
async def replym(event):
    if not event.is_group:
        return
    type = "ثروته"
    await botuse(type)
    r = await event.get_reply_message()
    uid = str(r.sender_id)
    gid = str(event.chat_id)
    if uid in points:
        m = points[uid][gid]['points']
    else:
        m = 0
    await event.reply(f'فلوسه ↢ ( `{m}` )')
@ABH.on(events.NewMessage(pattern=r'^حول (\d+(\.\d+)?)'))
async def send_money(event):
    if not event.is_group:
        return
    type = "حول"
    await botuse(type)
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
    if str(user1_id) not in points:
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
