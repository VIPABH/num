from ABH import ABH #type: ignore
from datetime import datetime
from telethon import events
from other import botuse
from Resources import *
import os, json, pytz
from Program import *
DATA_FILE = "counts.json"
def load_data():
    if not os.path.exists(DATA_FILE):
        return {"اليومي": {}, "الاسبوعي": {}, "last_daily": "", "last_weekly": ""}
    try:
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except json.JSONDecodeError:
        os.rename(DATA_FILE, DATA_FILE + ".broken")
        return {"اليومي": {}, "الاسبوعي": {}, "last_daily": "", "last_weekly": ""}
def save_data(data):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
count = load_data()
async def unified_handler(event):
    if not event.is_group:
        return
    baghdad_tz = pytz.timezone("Asia/Baghdad")
    now = datetime.now(baghdad_tz)
    current_time = now.strftime("%H:%M")
    current_date = now.strftime("%Y-%m-%d")
    weekday = now.weekday()
    unm = str(event.sender_id)
    guid = str(event.chat_id)
    if current_time == "00:00" and current_date != count.get("last_daily"):
        count["اليومي"] = {}
        count["last_daily"] = current_date
    if weekday == 4 and current_time == "00:00" and current_date != count.get("last_weekly"):
        count["الاسبوعي"] = {}
        count["last_weekly"] = current_date
    if guid not in count["اليومي"]:
        count["اليومي"][guid] = {}
    if guid not in count["الاسبوعي"]:
        count["الاسبوعي"][guid] = {}
    if unm not in count["اليومي"][guid]:
        count["اليومي"][guid][unm] = 0
    if unm not in count["الاسبوعي"][guid]:
        count["الاسبوعي"][guid][unm] = 0
    count["اليومي"][guid][unm] += 1
    count["الاسبوعي"][guid][unm] += 1
    save_data(count)
@ABH.on(events.NewMessage(pattern="^عدد (المتفاعلين|تفاعل)$"))
async def show_interactions(e):
    if not e.is_group:
        return
    t = e.text
    if t == "عدد المتفاعلين":
        await botuse(t)
        guid = str(e.chat_id)
        action = "اليومي"
    else:
        await botuse(t)
        guid = str(e.chat_id)
        action = "الاسبوعي"
    if guid in count[action]:
        await chs(e, f"تفاعل الاعضاء {action}: {len(count[action][guid])} عضو")
@ABH.on(events.NewMessage(pattern="^توب اليومي|المتفاعلين$"))
async def اليومي(event):
    if not event.is_group:
        return
    type = "المتفاعلين"
    await botuse(type)
    guid = str(event.chat_id)
    if guid not in count or not count[guid]:
        await event.reply("لا توجد بيانات لعرضها.")
        await react(event, "💔")
        return
    sorted_users = sorted(
        count["اليومي"][guid].items(),
        key=lambda x: x[1],
        reverse=True
    )[:10]
    top_users = []
    for idx, (uid, msg_count) in enumerate(sorted_users, 1):
        try:
            user = await event.client.get_entity(int(uid))
            fname = user.first_name or "مجهول"
        except:
            fname = "مجهول"
        top_users.append(f"{idx}. {fname} - {msg_count} رسالة")
    x = await event.reply("\n".join(top_users))
    await react(event, "🌚")
@ABH.on(events.NewMessage(pattern="^توب الاسبوعي|تفاعل$"))
async def الاسبوعي(event):
    if not event.is_group:
        return
    type = "تفاعل"
    await botuse(type)
    guid = str(event.chat_id)
    if guid not in count or not count[guid]:
        await event.reply("لا توجد بيانات لعرضها.")
        await react(event, "💔")
        return
    sorted_users = sorted(
        count["الاسبوعي"][guid].items(),
        key=lambda x: x[1],
        reverse=True
    )[:10]
    top_users = []
    for idx, (uid, msg_count) in enumerate(sorted_users, 1):
        try:
            user = await event.client.get_entity(int(uid))
            fname = user.first_name or "مجهول"
        except:
            fname = "مجهول"
        top_users.append(f"{idx}. {fname} - {msg_count} رسالة")
    x = await event.reply("\n".join(top_users))
    await react(event, "👍")
@ABH.on(events.NewMessage(pattern=r'^(رسائله|رسائلة|الرسائل|رسائلي)$'))
async def his_res(event):
    if event.text in ('رسائلي', 'الرسائل'):
        unm1 = str(event.sender_id)
        guid1 = str(event.chat_id)
    else:
      r = await event.get_reply_message()  
      if not r:
          await react(event, "🤔")
          return
      unm1 = str(r.sender_id)
      guid1 = str(event.chat_id)
    type = "رسائله"
    await botuse(type)
    if guid1 in count and unm1 in count[guid1]:
        msg_count = count["اليومي"][guid1][unm1]
        الاسبوعي = count["الاسبوعي"][guid1][unm1]
        x = await info(event, None)
        الكلي = x.get("الرسائل", 0)
        await react(event, "👍")
        await chs(event, f'اليوميه: {msg_count}\nالاسبوعية: {الاسبوعي}\nالكليه: {الكلي}')
@ABH.on(events.NewMessage(pattern='^اوامر التوب$'))
async def title(event):
    if not event.is_group:
        return
    type = "اوامر التوب"
    await botuse(type)
    await event.reply('اهلا صديقي , اوامر الرسائل \n ارسل `المتفاعلين` | `توب اليومي` ل اضهار توب 15 تفاعل \n ارسل `تفاعل` | `توب الاسبوعي` ل اظهار تفاعل المجموعه في اسبوع \n ارسل `رسائلي` ل اضهار رسائلك في اخر يوم \n ارسل `رسائله` ل اضهار رساله الشخص بالرد \n استمتع')
