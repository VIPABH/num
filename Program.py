from telethon import events, Button
import asyncio, os, sys, random
import json, redis, subprocess
from Resources import *
from other import *
from ABH import ABH
@ABH.on(events.NewMessage(pattern='^اوامر|اوامري$'))
async def myhandlers(event):
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
            Button.inline('اوامر التنظيف', data='d'),
            Button.inline('اوامر الفلوس', data='m')
        ],
        [
            Button.inline('اوامر اليوت', data='yt'),
            Button.url('تحديثات البوت', url=f'https://t.me/{ch}')
        ]
    ]
    await event.reply('شتريد من الاوامر متكلي ', buttons=buttons)
@ABH.on(events.callbackquery)
async def callbacklist(event):
    data = event.data.decode('utf-8')
    print(data)
    if data == 'gaurd':
        await event.edit('**اوامر الحماية**\n `التقييد` `تعطيل` | `تفعيل` \n `تقييد عام` | `مخفي قيده` \n لتقييد المستخدم مده 20 دقيقه \n التقييد ما راح ينرفع الا بعد العشرين دقيقه \n الامر يشتغل ل `المعاونين` والاعضاء تكدر تقيد مقابل 100 الف مدة 30 ثانية. \n امر التقييد التلقائي , يمنع الفشار \n التشغيل `التقييد تفعيل`')
    elif data == 'ADD':
        await event.edit('**اوامر الرفع والتنزيل** \n `ترقية` لرفع المستخدم مشرف حسب الصلاحيات الي راح تحددها اله \n `تغيير لقبي` يغير لقب المشرف اذا جان مخفي رافعه فقط \n `رفع سمب` اقل مبلغ تكدر ترفع بي 1000 تكدر تشوف السمبات عن طريق `السمبات` \n تكدر تنزله عن طريق `تنزيل سمب`.')
    elif data == 'g':
        await event.edit(r"""**اوامر الالعاب** 
/num 
لتشغيل لعبة الارقام 
فكرتها لازم تحزر الرقم من 10 ب 3 محاولات 

/ring 
لتشغيل لعبة محيبس 
فكرتها لازم تحزر المحبس وين موجود ب يا ايد 
عبر امري `طك` `جيب` 

/football 
لعبة تخليك تحزر الاعب حسب الصوره 

`كره قدم` 
لتشغيل لعبة اسئلة رياضية 
اسئلة رياضية متنوعه مستوى صعوبتها عالي

`اكس او` \xo 
تشغيل لعبة xo ب تسع ازرار انلاين لعبة pvp 😁 

`اسئلة` تشغيل اسئلة شيعيه دينيه مستوى صعوبه عالي 

`حجرة` /rock `مضاربة`
لعبة حجرة ورقه مقص 
اذا الامر كان رد فراح تلعب pvp اما اذا كان بدون رد فراح تلعب ضد البوت  

`اسرع` 
لعبة اسرع 
فكرتها تدخل مجموعه تتنافس على اسرع شخص يحزر الكلمه 
الامر مدعوم ب خمس جولات لكل جوله فائز

`كتويت` يرسل لك اسئلة عشوائيه خفيفه بي 180 سؤال

`غموض` فكره اللعبه غير مطروقة 
تدخل مجموعه تلعب واي شخص يسوي رد ل اي رساله راح يخسر 
تحتمل واحد فقط للفوز 
بالرد على مستخدم + ب تحديد مبلغ مادي 
راح البوت يختار شخص يفوز العدد الي حددته انت وشخص يخسر 
ف لو انت كتبت مضاربة 10 وفزت فراح تربح 20 والشخص يخسر 10
""")
    elif data == 'c':
        await event.edit('**اوامر التوب** \n `المتفاعلين` | `التوب اليومي` \n يرسل لك توب 10 تفاعل من ساعه 12 صباحا \n يترست ساعه 12 \n \n `تفاعل` | `التوب الاسبوعي` \n يرسل لك توب 10 تفاعل اسبوعي \n يترست كل جمعة ساعة 12 صباحا')
    elif data == 'd':
        await event.edit('**اوامر التنظيف** \n `امسح` | `تنظيف` يمسح الرسائل المخزنه للحذف بالتسلسل \n `التنظيف تفعيل` | `تعطيل` \n عند التفعيل البوت راح يحذف الرسائل الموجهه للحذف من يصير عددها 150 **الحذف تلقائي** \n `تفريغ` \n يتخطى مسح الرسائل المحفوظة ويتجاهل مسحها كلها \n `ثبتها` | `تخطي المسح` \n يتخطى مسح الرساله بالرد \n `عدد` | `كشف ميديا` \n يظهرلك عدد الرسائل الموجهه للحذف \n ')
    elif data == 'm':
        await event.edit('**اوامر الفلوس** \n `الاغنياء` \n ل اظهار عدد اكثر 10 اشخاص عندهم فلوس بالمجموعه \n \n `ثروتي` \n يظهرلك عدد فلوسك بالبوت\n \n `ثروته` \n يظهرلك ثروه الشخص الي سويت عليه رد \n\n `حول` \n بالرد على مستخدم مع تحديد عدد مادي لتحويله للمستخدم \n\n')
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
        except Exception as event:
            await hint(f"⚠️ حدث خطأ أثناء التحقق من الصلاحيات: {event}")
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
    ch = r.get(CHANNEL_KEY)
    buttons = Button.url('🫆', url=f'https://t.me/{ch}')
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
