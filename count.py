from ABH import ABH #type: ignore
from datetime import datetime
from telethon import events
from other import botuse
from Resources import *
import os, json, pytz
from Program import *
DATA_FILE = "uinfo.json"
DATA_FILE_WEAK = "uinfoWEAK.json"
DAILY_RESET_FILE = "daily_reset.json"
WEEKLY_RESET_FILE = "weekly_reset.json"
def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}
def save_data(data):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
def load_json(file_path, default_value=None):
    if not os.path.exists(file_path):
        return default_value
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            return json.load(f)
    except json.JSONDecodeError as e:
        print(f"[تحذير] فشل تحميل JSON من {file_path} بسبب: {e}")
        os.rename(file_path, file_path + ".broken")
        return default_value
def save_json(file_path, data):
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)
def try_fix_json_file(file_path):
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            return json.load(f)
    except json.JSONDecodeError as e:
        print(f"[تحذير] فشل تحميل JSON بسبب: {e}")
        print("[...] محاولة تصحيح الملف تلقائيًا")
    fixed_lines = []
    with open(file_path, "r", encoding="utf-8") as f:
        lines = f.readlines()
    for i in range(len(lines)):
        temp = "".join(fixed_lines + lines[i + 1 :])
        try:
            json.loads(temp)
            with open(file_path, "w", encoding="utf-8") as f_out:
                f_out.write(temp)
            return json.loads(temp)
        except json.JSONDecodeError:
            fixed_lines.append(lines[i])
    return {}
def last_daily_reset_date():
    data = load_json(DAILY_RESET_FILE, {})
    return data.get("date", None)
def update_daily_reset_date(date_str):
    save_json(DAILY_RESET_FILE, {"date": date_str})
def last_reset_date():
    data = load_json(WEEKLY_RESET_FILE, {})
    return data.get("date", None)
def update_reset_date(date_str):
    save_json(WEEKLY_RESET_FILE, {"date": date_str})
uinfo = load_json(DATA_FILE, {})
WEAK = load_json(DATA_FILE_WEAK, {})
async def unified_handler(event):
    global uinfo, WEAK
    if not event.is_group:
        return
    baghdad_tz = pytz.timezone("Asia/Baghdad")
    now = datetime.now(baghdad_tz)
    current_time = now.strftime("%H:%M")
    current_date = now.strftime("%Y-%m-%d")
    weekday = now.weekday()
    unm = str(event.sender_id)
    guid = str(event.chat_id)
    if guid not in uinfo:
        uinfo[guid] = {}
    if guid not in WEAK:
        WEAK[guid] = {}
    if weekday == 4 and current_time == "00:00" and current_date != last_reset_date():
        WEAK = {}
        save_json(DATA_FILE_WEAK, WEAK)
        update_reset_date(current_date)
    if current_time == "00:00" and current_date != last_daily_reset_date():
        for gid in uinfo:
            for uid in uinfo[gid]:
                uinfo[gid][uid] = 0
        save_data(uinfo)
        update_daily_reset_date(current_date)
    if unm not in uinfo[guid]:
        uinfo[guid][unm] = 0
    uinfo[guid][unm] += 1
    save_json(DATA_FILE, uinfo)
    if unm not in WEAK[guid]:
        WEAK[guid][unm] = 0
    WEAK[guid][unm] += 1
    save_json(DATA_FILE_WEAK, WEAK)
@ABH.on(events.NewMessage(pattern="^توب اليومي|المتفاعلين$"))
async def اليومي(event):
    if not event.is_group:
        return
    type = "المتفاعلين"
    await botuse(type)
    guid = str(event.chat_id)
    if guid not in uinfo or not uinfo[guid]:
        await event.reply("لا توجد بيانات لعرضها.")
        await react(event, "💔")
        return
    sorted_users = sorted(
        uinfo[guid].items(),
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
    if guid not in WEAK or not WEAK[guid]:
        await event.reply("لا توجد بيانات لعرضها.")
        await react(event, "💔")
        return
    sorted_users = sorted(
        WEAK[guid].items(),
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
    if guid1 in uinfo and unm1 in uinfo[guid1]:
        msg_count = uinfo[guid1][unm1]
        الاسبوعي = WEAK[guid1][unm1]
        x = await info(event, None)
        await hint(f'{x}')
        الكلي = x[guid1][unm1]['الرسائل']
        await react(event, "👍")
        await chs(event, f'{event.text} \n اليوميه: {msg_count} \n الاسبوعية: {الاسبوعي} \n الكليه: {الكلي}')
@ABH.on(events.NewMessage(pattern='^اوامر التوب$'))
async def title(event):
    if not event.is_group:
        return
    type = "اوامر التوب"
    await botuse(type)
    await event.reply('اهلا صديقي , اوامر الرسائل \n ارسل `المتفاعلين` | `توب اليومي` ل اضهار توب 15 تفاعل \n ارسل `تفاعل` | `توب الاسبوعي` ل اظهار تفاعل المجموعه في اسبوع \n ارسل `رسائلي` ل اضهار رسائلك في اخر يوم \n ارسل `رسائله` ل اضهار رساله الشخص بالرد \n استمتع')
