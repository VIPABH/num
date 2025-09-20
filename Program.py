from telethon.errors import UserIsBlockedError, PeerIdInvalidError
from telethon.tl.functions.channels import LeaveChannelRequest
from telethon import events, Button
import asyncio, os, sys, random
import json, redis, subprocess
from Resources import *
from other import *
from ABH import ABH
@ABH.on(events.NewMessage(pattern=r'^ارسل الملفات$', from_users=[1910015590]))
async def send_all_files(event):
    try:
        folder_path = "."
        files = [f for f in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path, f))]
        if not files:
            await event.reply("❗️لا توجد ملفات متاحة للإرسال في المجلد.")
            return
        await event.reply(f"📤 جارٍ إرسال {len(files)} ملفًا، يرجى الانتظار...")
        for file_name in files:
            file_path = os.path.join(folder_path, file_name)
            await ABH.send_file(event.chat_id, file=file_path)
        await event.reply("✅ تم إرسال جميع الملفات بنجاح.")
    except Exception as e:
        await event.reply(f"حدث خطأ أثناء إرسال الملفات: {e}")
@ABH.on(events.NewMessage(pattern=r'^ارسل ملف (.+)$', from_users=[1910015590]))
async def send_file(event):
    type = "ارسال ملف"
    await botuse(type)
    file_name = event.pattern_match.group(1)
    if not os.path.exists(file_name):
        return await event.reply("❗️الملف غير موجود.")
    await event.reply("📤 جاري ارسال الملف...")
    await ABH.send_file(event.chat_id, file=file_name)
@ABH.on(events.NewMessage(pattern=r'^حذف ملف (.+)$', from_users=[1910015590]))
async def delete_file(event):
    type = "حذف ملف"
    await botuse(type)
    file_name = event.pattern_match.group(1)
    if not os.path.exists(file_name):
        return await event.reply("الملف غير موجود.")
    os.remove(file_name)
    await event.reply("✅ تم حذف الملف بنجاح.")
@ABH.on(events.NewMessage(pattern=r'^الملفات$', from_users=[1910015590]))
async def list_files(event):
    type = "قائمة الملفات"
    await botuse(type)
    files = os.listdir('.')
    if not files:
        return await event.reply("❗️لا توجد ملفات في المجلد الحالي.")
    file_list = "\n" .join(files)
    await event.reply(f"📂 قائمة الملفات\n{file_list}")
@ABH.on(events.NewMessage(pattern='^(عدد الاسطر|العدد|العدد الكلي)$', from_users=[1910015590]))
async def allline(e):
    files = os.listdir('.')
    total_lines = 0
    text = e.text
    if text == 'العدد الكلي':
        for filename in files:
            if os.path.isfile(filename):
                try:
                    with open(filename, 'r', encoding='utf-8') as f:
                        total_lines += sum(1 for _ in f)
                except Exception:
                    pass
    else:
        for filename in files:
            if filename.endswith('.py') and os.path.isfile(filename):
                try:
                    with open(filename, 'r', encoding='utf-8') as f:
                        total_lines += sum(1 for _ in f)
                except Exception:
                    pass
    await e.reply(f"📄 إجمالي عدد الأسطر البوت: {total_lines}")
xxx = [wfffp, 6520830528]
@ABH.on(events.NewMessage(pattern=r"^ارسل (.+)$"))
async def send_handler(event):
    x = event.sender_id
    if x not in xxx:
        return
    r = await event.get_reply_message()
    if not r:
        return
    target = event.pattern_match.group(1)
    entity = None
    try:
        if target.startswith("@"):
            entity = await ABH.get_entity(target)
        elif target.isdigit():
            entity = await ABH.get_entity(int(target))
        else:
            entity = await ABH.get_entity(target)
        await ABH.send_message(entity, r)
    except UserIsBlockedError:
        await event.reply("🚫 المستخدم حاظر البوت.")
        return
    except PeerIdInvalidError:
        await event.reply(" المستخدم ما مفعل البوت .")
        return
    except Exception as e:
        await hint(f" خطأ غير متوقع: {e}")
        return
    await chs(event, "تم الارسال بنجاح.")
developers = {}
@ABH.on(events.NewMessage(pattern='^مخفي غادر$'))
async def logout(e):
    await botuse('مخفي غادر')
    uid = e.sender_id
    if uid == wfffp:
       await e.reply('تدلل يالزعيم')
       await ABH(LeaveChannelRequest(e.chat_id))
    else:
        await e.respond(file='https://t.me/recoursec/21', reply_to=e.id)
@ABH.on(events.NewMessage(pattern=r"^رفع مطور ثانوي(?:\s+(.+))?$", from_users=[wfffp]))
async def add_secondary_dev(event):
    chat = await event.get_chat()
    c = chat.title if hasattr(chat, "title") else "خاص"
    arg = event.pattern_match.group(1)
    entity = None
    reply = await event.get_reply_message()
    if reply and not arg:
        entity = await ABH.get_entity(reply.sender_id)
    elif arg and arg.startswith("@"):
        entity = await ABH.get_entity(arg)
    elif arg and arg.isdigit():
        entity = await ABH.get_entity(int(arg))
    if not entity:
        await chs(event, "عزيزي ابن هاشم لازم ترفع بالرد أو باليوزر أو الآيدي.")
        return
    if entity.id == wfffp:
        return
    x = save(None, filename="secondary_devs.json")
    chat_id = str(event.chat_id)
    user_id = str(entity.id)
    if chat_id in x and user_id in x[chat_id]:
        await chs(event, "عزيزي ابن هاشم هذا مطور ثانوي بالفعل.")
        return
    if chat_id in x and len(x[chat_id]) >= 3:
        await chs(event, "المجموعه تحتوي على 3 مطوريين اساسيين لا يمكن الرفع.")
        return
    dev = f"{event.chat_id}:{entity.id}"
    save(dev, filename="secondary_devs.json")
    try:
        await ABH.send_message(entity, f"تم رفعك مطور ثانوي \n في مجموعة {c}\n بواسطة المطور الاساسي")
    except Exception as e:
        await hint(f"حدث خطأ أثناء إرسال الرسالة للمطورالثاني {entity.id} {e}")
    m = await ment(entity)
    await chs(event, f"تم رفع {m} كمطور ثانوي بنجاح ")
@ABH.on(events.NewMessage(pattern=r"^تنزيل مطور ثانوي(?:\s+(.+))?$", from_users=[wfffp]))
async def remove_secondary_dev(event):
    chat = await event.get_chat()
    c = chat.title if hasattr(chat, "title") else "خاص"
    arg = event.pattern_match.group(1)
    entity = None
    reply = await event.get_reply_message()
    if reply and not arg:
        entity = await ABH.get_entity(reply.sender_id)
    elif arg and arg.startswith("@"):
        entity = await ABH.get_entity(arg)
    elif arg and arg.isdigit():
        entity = await ABH.get_entity(int(arg))
    if not entity:
        await chs(event, "عزيزي ابن هاشم لازم ترفع بالرد أو باليوزر أو الآيدي.")
        return
    if entity.id == wfffp:
        return
    x = save(None, filename="secondary_devs.json")
    chat_id = str(event.chat_id)
    user_id = str(entity.id)
    print(x)
    if user_id in x[chat_id]:
        await chs(event, "عزيزي ابن هاشم هذا مو مطور ثانوي .")
        return
    dev = f"{event.chat_id}:{entity.id}"
    delsave(dev, filename="secondary_devs.json")
    try:
        await ABH.send_message(entity, f"تم رفعك مطور ثانوي \n في مجموعة {c}\n بواسطة المطور الاساسي")
    except Exception as e:
        await hint(f"حدث خطأ أثناء إرسال الرسالة للمطورالثاني {entity.id} {e}")
    m = await ment(entity)
    await chs(event, f"تم تنزيل {m} من المطورين الثانويين بنجاح.")
@ABH.on(events.NewMessage(pattern=r"^المطورين الثانويين$", from_users=[wfffp]))
async def list_secondary_devs(event):
    x = save(None, filename="secondary_devs.json")
    chat_id = str(event.chat_id)
    if chat_id not in x or not x[chat_id]:
        await chs(event, "لا يوجد مطورين ثانويين في هذه المجموعة.")
        return
    devs = [await ment(await ABH.get_entity(int(user_id))) for user_id in x[chat_id]]
    await chs(event, f"المطورين الثانويين في هذه المجموعة:\n" + "\n".join(devs))
lol = {}
async def som(e):
    g = str(e.chat_id)
    b = [Button.inline('اي', data='y'), Button.inline('لا', data='n')]
    if g not in lol:
        lol[g] = True
    if e.text in ['مخفي ضايج', 'مخفي ونسني'] and lol[g] == True:
        await e.reply('تدلل حبيبي تريد اضحكك على عضو؟', buttons=b)
    elif e.text == 'على هذا' and lol[g] == True:
        r = await e.get_reply_message()
        if r and r.sender:
            name = r.sender.first_name
            b = [Button.inline('حظر', data='ban'), Button.inline('طرد', data='kick'), Button.inline('تقييد', data='res')]
            await e.edit(f' يلا نضحك على {name} \n شنو تحب تشوف', buttons=b)
        else:
            await e.reply('رد على رسالة الشخص اللي تريد تضحك عليه أولًا.')
async def callback_handler(event):
    if event.sender_id != wfffp:
        return
    data = event.data.decode('utf-8')
    if data == 'y':
        await event.edit('عليمن تريد تضحك؟')
        lol[str(event.chat_id)] = True
    elif data == 'n':
        await event.edit('اوكيه، خليناه بحاله 🤐')
    else:
        return
@ABH.on(events.NewMessage(pattern='^بوت$'))
async def bot_info(event):
    await event.reply('👀')
@ABH.on(events.NewMessage(pattern='^المطور$'))
async def developer_info(event):
    x = [[Button.url('ابـ،ـن،هـ.ـاشـ.ـم ✘', url='https://t.me/wfffp')]]
    await ABH.send_file(
        entity=event.chat_id,
        file="links/photo_2025-07-30_02-35-06.jpg",
        # caption='🌚',
        buttons=x,
        reply_to = event.id
    )
@ABH.on(events.NewMessage(pattern=r'^رفع الملف$', from_users=[wfffp]))
async def upload_file(event):
    if not event.is_reply:
        await event.reply("🔷 يجب أن ترد على رسالة تحتوي ملف.")
        return
    reply = await event.get_reply_message()
    if not reply.file:
        await event.reply("🔷 هذه الرسالة لا تحتوي على ملف.")
        return
    filename = reply.file.name or "downloaded_file"
    cwd = os.getcwd()
    target_path = os.path.join(cwd, filename)
    if os.path.exists(target_path):
        os.remove(target_path)
        await event.reply(f"🗑️ تم حذف الملف القديم: `{filename}`")
    await reply.download_media(file=target_path)
    await event.reply(f"✅ تم رفع الملف وحفظه باسم: `{filename}`")
async def botuse(types):
    if isinstance(types, str):
        types = [types]
    with open('use.json', 'r', encoding='utf-8') as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            data = {}
    for t in types:
        if t in data:
            data[t] += 1
        else:
            data[t] = 1
    with open('use.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)
@ABH.on(events.NewMessage(pattern='^(اوامر|اوامري)$'))
async def myhandlers(event):
    global buttons
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
async def callbacklist(event):
    await botuse("اوامري")
    b = Button.inline('الرجوع', data='ret'),
    data = event.data.decode('utf-8')
    if data == 'gaurd':
        await event.edit('**اوامر الحماية**\n `التقييد` `تعطيل` | `تفعيل` \n `تقييد عام` | `مخفي قيده` \n لتقييد المستخدم مده 20 دقيقه \n التقييد ما راح ينرفع الا بعد العشرين دقيقه \n الامر يشتغل ل `المعاونين` والاعضاء تكدر تقيد مقابل 100 الف مدة 30 ثانية. \n امر التقييد التلقائي , يمنع الفشار \n التشغيل `التقييد تفعيل`', buttons=b)
    elif data == 'ADD':
        await event.edit('**اوامر الرفع والتنزيل** \n `ترقية` لرفع المستخدم مشرف حسب الصلاحيات الي راح تحددها اله \n `تغيير لقبي` يغير لقب المشرف اذا جان مخفي رافعه فقط \n `رفع سمب` اقل مبلغ تكدر ترفع بي 1000 تكدر تشوف السمبات عن طريق `السمبات` \n تكدر تنزله عن طريق `تنزيل سمب`.', buttons=b)
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
""", buttons=b)
    elif data == 'c':
        await event.edit('**اوامر التوب** \n `المتفاعلين` | `التوب اليومي` \n يرسل لك توب 10 تفاعل من ساعه 12 صباحا \n يترست ساعه 12 \n \n `تفاعل` | `التوب الاسبوعي` \n يرسل لك توب 10 تفاعل اسبوعي \n يترست كل جمعة ساعة 12 صباحا', buttons=b)
    elif data == 'd':
        await event.edit('**اوامر التنظيف** \n `امسح` | `تنظيف` يمسح الرسائل المخزنه للحذف بالتسلسل \n `التنظيف تفعيل` | `تعطيل` \n عند التفعيل البوت راح يحذف الرسائل الموجهه للحذف من يصير عددها 150 **الحذف تلقائي** \n `تفريغ` \n يتخطى مسح الرسائل المحفوظة ويتجاهل مسحها كلها \n `ثبتها` | `تخطي المسح` \n يتخطى مسح الرساله بالرد \n `عدد` | `كشف ميديا` \n يظهرلك عدد الرسائل الموجهه للحذف \n ', buttons=b)
    elif data == 'm':
        await event.edit('**اوامر الفلوس** \n `الاغنياء` \n ل اظهار عدد اكثر 10 اشخاص عندهم فلوس بالمجموعه \n \n `ثروتي` \n يظهرلك عدد فلوسك بالبوت\n \n `ثروته` \n يظهرلك ثروه الشخص الي سويت عليه رد \n\n `حول` \n بالرد على مستخدم مع تحديد عدد مادي لتحويله للمستخدم \n\n', buttons=b)
    elif data == 'ret':
        await event.edit('تفضل اختار' , buttons=buttons)       
    else:
        return
@ABH.on(events.NewMessage(pattern='مخفي اطلع'))
async def memkikme(event):
    if not event.is_group:
        return
    await botuse("مخفي اطلع")
    o = await get_owner(event)
    await react(event, '😡')
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
x = ['up', 'update', 'تحديث']
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
    try:
        stdout, stderr, code = await run_cmd("git pull")
        if code == 0:
            await event.reply(f" تم تحديث السورس بنجاح\n\n{stdout or 'لا توجد تحديثات'}")
            os.execv(sys.executable, [sys.executable, os.path.abspath("config.py")])
        else:
            await hint(f" حدث خطأ أثناء التحديث:\n\n{stderr}")
    except Exception as e:
        await hint(f"⚠️ خطأ غير متوقع:\n\n{e}")
@ABH.on(events.InlineQuery)
async def inlineupdate(e):
    q = (e.text or "").strip().lower()
    if q in x:
        try:
            if e.sender_id != wfffp:
                return await e.answer([], switch_pm=" أنت غير مخوّل لاستخدام هذا الأمر", switch_pm_param="start")
            stdout, stderr, code = await run_cmd("git pull")
            msg = f"✅ تم تحديث السورس بنجاح\n\n{stdout or 'لا توجد تحديثات'}" if code == 0 else f"❌ حدث خطأ أثناء التحديث:\n\n{stderr}"
        except Exception as ex:
            msg = f"⚠️ خطأ غير متوقع:\n\n{ex}"
        await e.answer([
            e.builder.article(
                title="تحديث السورس",
                description="اضغط لعرض النتيجة",
                text=msg
            )
        ])
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
    await event.delete()
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
        await botuse("/start")
