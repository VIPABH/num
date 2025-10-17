from telethon import events, Button
from num2words import num2words
from other import botuse
from Resources import *
from ABH import ABH
import json
wfffp = 1910015590
lit = [6498922948, 7176263278, 6520830528, 49820009]
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
    uid = str(uid)
    if uid not in points:
        points[uid] = 0
    points[uid] += amount
    save_points(points)
# def add_user(uid, gid, name, rose, amount):
#     uid, gid = str(uid), str(gid)
#     if gid not in rose:
#         rose[gid] = {}
#     if uid not in rose[gid]:
#         rose[gid][uid] = {
#             "name": name,
#             "status": "عادي",
#             "giver": None,
#             "m": amount,
#             "promote_value": 0
#         }
def delpoints(uid, gid, points, amount):
    uid = str(uid)
    if uid not in points:
        points[uid] = 0
    points[uid] -= amount
    save_points(points)
@ABH.on(events.NewMessage(pattern='^الاغنياء$'))
async def show_rich(event):
    if not points:
        await event.reply("لا توجد بيانات ثروة حالياً.")
        return
    valid_points={uid:val for uid,val in points.items() if isinstance(val,int)}
    if not valid_points:
        await event.reply("لا توجد بيانات صالحة حالياً.")
        return
    sorted_points=sorted(valid_points.items(),key=lambda x:x[1],reverse=True)
    top_rich=sorted_points[:10]
    message="💰 أغنى الأشخاص في البوت 💰\n\n"
    for i,(uid,amt) in enumerate(top_rich,start=1):
        try:
            user=await event.client.get_entity(int(uid))
            name=user.first_name if user.first_name else "بدون اسم"
        except:
            name=f"مستخدم {uid}"
        message+=f"{i}. {name} → `{amt:,}`\n"
    await event.reply(message)
@ABH.on(events.NewMessage(pattern=r'^اضف فلوس (\d+)$'))
async def add_money(event):
    if not event.is_group:
        return
    type = "اضف فلوس"
    await botuse(type)
    r = await event.get_reply_message()
    uid = event.sender_id
    x = save(None, 'secondary_devs.json')
    chat = str(event.chat_id)
    if not (wfffp == uid or uid in lit):
        return
    if (r.sender_id == event.sender_id and uid != wfffp):
        await event.reply("هههههه")
        return
    p = int(event.pattern_match.group(1))
    gid = event.chat_id
    user_id = r.sender_id
    add_points(user_id, gid, points, amount=p)
    await event.reply(f"تم اضافة {p} دينار ل {r.sender.first_name}")
@ABH.on(events.NewMessage(pattern=r'^حذف فلوس (\d+)$'))
async def add_money(event):
    if not event.is_group:
        return
    if not (wfffp == uid or uid in lit):
        return
    type = "حذف فلوس"
    r = await event.get_reply_message()
    await botuse(type)
    uid = event.sender_id
    x = save(None, 'secondary_devs.json')
    chat = str(event.chat_id)
    if (r.sender_id == event.sender_id and uid != wfffp):
        await event.reply("هههههه")
        return
    p = int(event.pattern_match.group(1))
    gid = event.chat_id
    user_id = r.sender_id
    delpoints(user_id, gid, points, amount=p)
    await event.reply(f"تم حذف {p} دينار ل {r.sender.first_name}")
@ABH.on(events.NewMessage(pattern=r'^تصفير$'))
async def add_money(event):
    if not event.is_group:
        return
    r = await event.get_reply_message()
    type = "تصفير"
    await botuse(type)
    uid = event.sender_id
    x = save(None, 'secondary_devs.json')
    chat = str(event.chat_id)
    if not (wfffp == uid or uid in lit or chat in x and str(uid) in x[chat]):
        return
    if (r.sender_id == event.sender_id and uid != wfffp):
        await event.reply("هههههه")
        return
    uid = str(r.sender_id)
    gid = str(event.chat_id)
    p = points[uid]
    delpoints(str(uid), str(gid), points, amount=int(p))
    await event.reply(f"تم حذف {p} دينار لـ {r.sender.first_name}")
@ABH.on(events.NewMessage(pattern='ثروتي'))
async def m(event):
    if not event.is_group:
        return
    type = "ثروتي"
    await botuse(type)
    uid = str(event.sender_id)
    b = Button.inline("اضغط هنا لعرضها رقم", data='moneymuch')
    if uid in points:
        m = points[uid] 
    else:
        m = 0
    arabic_text = num2words(m, lang='ar')
    await event.reply(f'فلوسك ↢ {m} \n ( `{arabic_text}` )', buttons=b)
@ABH.on(events.NewMessage(pattern='ثروته|الثروه'))
async def replym(event):
    if not event.is_group:
        return
    type = "ثروته"
    await botuse(type)
    r = await event.get_reply_message()
    uid = str(r.sender_id)
    gid = str(event.chat_id)
    b = Button.inline("اضغط هنا لعرضها رقم", data='moneymuch')
    if uid in points:
        m = points[uid]
    else:
        m = 0
    arabic_text = num2words(m, lang='ar')
    await event.reply(f'فلوسه ↢ {m} \n ( `{arabic_text}` )', buttons=b)
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
    if str(user1_id) not in points:
        await event.reply("ليس لديك نقاط كافية.")
        return
    if str(user2_id) not in points:
        points[str(user2_id)] = 0
    sender_points = points[str(user1_id)]
    if count > sender_points:
        await event.reply('رصيدك لا يكفي لهذا التحويل.')
        return
    delpoints(user1_id, event.chat_id, points, count)
    add_points(user2_id, event.chat_id, points, count)
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
