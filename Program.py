from telethon import events, Button
import asyncio, os, sys, random
import json, redis, subprocess
from Resources import *
from other import *
from ABH import ABH
@ABH.on(events.NewMessage(pattern='^اوامر|اوامري$'))
async def myhandlers(e):
    ch = r.get(CHANNEL_KEY)
    buttons = [
        [
            Button.inline('اوامر الحماية', data='gaurd'),
            Button.inline('اوامر الرفع', data='ADD')
        ],
        [
            Button.inline('اوامر الالعاب', data='g'),
            Button.inline('اوامر التفاعل', data='c')
        ],
        [
            Button.inline('اوامر المسح', data='d'),
            Button.inline('اوامر الفلوس', data='m')
        ],
        [
            Button.inline('اوامر اليوت', data='yt'),
            Button.url('تحديثات البوت', url=f'https://t.me/{ch}')
        ]
    ]
    await e.reply('شتريد من الاوامر متكلي ', buttons=buttons)
@ABH.on(events.ChatAction)
async def on_bot_added(event):
    if event.user_added or event.user_joined:
        if event.user_id == (await ABH.get_me()).id:
            await event.reply("يالفكر ضفتني عضو دضيفني مشرف شبيك")
    if (event.user_added or event.user_joined) and event.user_id == (await ABH.get_me()).id:
        try:
            participant = await ABH(GetParticipantRequest(
                channel=event.chat_id,
                participant='me'
            ))
            if participant.participant.rank or participant.participant.admin_rights:
                await event.reply("شكرا علئ الاشراف ضلعي")
            else:
                return
        except Exception as e:
            await hint(f"⚠️ حدث خطأ أثناء التحقق من الصلاحيات: {e}")
@ABH.on(events.NewMessage(pattern='مخفي اطلع'))
async def memkikme(event):
    if not event.is_group:
        return
    await botuse("مخفي اطلع")
    o = await get_owner(event)
    id = event.sender_id
    if id == o.id:
        await event.reply('هاي عود انت المالك')
        return
    elif id == wfffp:
        ء = random.choice(['مطور جيس حب انت', ' ها ابن هاشم سالمين'])
        await event.reply(ء)        
        return
    elif is_assistant(event.chat_id, event.sender_id):
        await event.reply('ديله عيني تره انزلك من المعاونين!!!')
        return
    elif not is_assistant(event.chat_id, event.sender_id):
        ء = random.choice(['توكل', 'مصدك نفسك يالعضو؟', 'هوه انت عضو تريد تطردني؟', 'طرد'])
        await event.reply(ء)
        return
@ABH.on(events.NewMessage(pattern="/screenlog|لوك", from_users=[wfffp]))
async def get_screen_log(event):
    session_name = "n"
    temp_log_file = "/tmp/log.txt"
    try:
        subprocess.run(
            ["screen", "-S", session_name, "-X", "hardcopy", "-h", temp_log_file],
            check=True
        )
        await ABH.send_file(
            wfffp,
            temp_log_file,
            caption="📄 آخر 500 سطر من شاشة البوت (screen)"
        )
        await chs(event, 'تم الارسال في الخاص')
    except subprocess.CalledProcessError:
        await event.respond("⚠️ حدث خطأ أثناء قراءة سجل screen.\nتحقق من اسم الجلسة أو صلاحيات الوصول.")
CHANNEL_KEY = 'x04ou'
r = redis.Redis(host='localhost', port=6379, db=0, decode_responses=True)
async def chs(event, c):
    buttons = Button.url('🫆', url=f'https://t.me/{CHANNEL_KEY}')
    await ABH.send_message(event.chat_id, c, reply_to=event.id, buttons=buttons)
async def run_cmd(command: str):
    process = await asyncio.create_subprocess_shell(
        command,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE
    )
    stdout, stderr = await process.communicate()
    return stdout.decode().strip(), stderr.decode().strip(), process.returncode
@ABH.on(events.NewMessage(pattern="^تحديث$", from_users=[wfffp]))
async def update_repo(event):
    stdout, stderr, code = await run_cmd("git pull")
    await asyncio.sleep(2)
    await event.reply(f" تحديث السورس بنجاح")
    if code == 0:
        os.execv(sys.executable, [sys.executable, "config.py"])
    else:
        await event.reply(f" حدث خطأ أثناء التحديث:\n\n{stderr}")
@ABH.on(events.NewMessage(pattern=r'^تعيين القناة (.+)', from_users=[wfffp]))
async def add_channel(event):
    global CHANNEL_KEY
    ch = event.pattern_match.group(1)
    x = r.exists(CHANNEL_KEY)
    await event.reply(f" تم اضافة قيمة القناة{ch}")
    if x:
        r.delete(CHANNEL_KEY)
    r.set(CHANNEL_KEY, ch)
    await event.reply(f" تم حفظ القناة {ch}")
    CHANNEL_KEY = ch
@ABH.on(events.NewMessage(pattern=r'^عرض القناة$', from_users=[wfffp]))
async def show_channel(event):
    ch = r.get(CHANNEL_KEY)
    if ch:
        await event.reply(f"📡 القناة المحفوظة: {ch}")
    else:
        await event.reply("⚠️ لا توجد قناة محفوظة.")
@ABH.on(events.NewMessage(pattern=r'^تفاعل البوت$', from_users=[wfffp]))
async def stats_handler(event):
    if event.sender_id != wfffp:
        return
    try:
        with open('use.json', 'r', encoding='utf-8') as f:
            data = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        await event.reply("لا توجد بيانات محفوظة بعد.")
        return
    if not data:
        await event.reply("📊 لا توجد أي استخدامات مسجلة بعد.")
        return
    msg = "📈 إحصائيات الاستخدام:\n\n"
    for key, value in sorted(data.items(), key=lambda item: item[1], reverse=True):
        msg += f"• {key} : {value}\n"
    x = event.is_private
    if x:
        await event.reply(msg)
    else:
        await ABH.send_message(wfffp, msg)
        await event.reply('تم الارسال في الخاص')
@ABH.on(events.NewMessage(pattern="^/start$"))
async def start(event):
    if event.is_private:
        buttons = [
            Button.url(
            "لرفعي مشرف",
                url="https://t.me/vipabh_bot?startgroup=Commands&admin=ban_users+delete_messages+restrict_members+invite_users+pin_messages+change_info+add_admins+promote_members+manage_call+manage_chat+manage_video_chats+post_stories+edit_stories+delete_stories"
    ),
            Button.url(
                "تحديثات البوت",
                url=f"https://t.me/{CHANNEL_KEY}"
    )
]
        await ABH.send_message(event.chat_id, "اهلا حياك الله \n مخفي لحماية المجموعة واوامر خدميه واللعاب جديدة \n علمود اشتغل بسلاسه لازم ترفعني مشرف عبر الزر الموجود 👇", buttons=buttons, reply_to=event.id)
