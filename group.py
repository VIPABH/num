from telethon.tl.functions.channels import  GetParticipantRequest
from telethon.tl.types import KeyboardButtonCallback
import google.generativeai as genai
from ABH import ABH, events #type: ignore
import  pytz
from googletrans import Translator
@ABH.on(events.NewMessage(pattern=r'كشف ايدي (\d+)'))
async def link(event):
    global user, uid
    uid = event.sender_id
    user_id = event.pattern_match.group(1)
    if not user_id:
        await event.reply("استخدم الأمر كـ `كشف ايدي 1910015590`")
        return
    try:
        user = await event.client.get_entity(int(user_id))
    except Exception as e:
        return await event.reply(f"لا يوجد حساب بهذا الآيدي...")
    tag = user.first_name.replace("\u2060", "") if user.first_name else user.username
    button = KeyboardButtonCallback("تغيير الئ رابط", b"recgange")
    await event.reply(f"⌔︙[{tag}](tg://user?id={user.id})", buttons=[button])
@ABH.on(events.CallbackQuery(data=b"recgange"))
async def chang(event):
    global user, uid
    sender_id = event.sender_id 
    if sender_id != uid:
        await event.answer("شلون وي الحشريين احنة \n عزيزي الامر خاص بالمرسل هوه يكدر يغير فقط😏", alert=True)
        return
    if uid is not None and sender_id == uid:
        await event.edit(f"⌔︙رابط المستخدم: tg://user?id={user.id}")
timezone = pytz.timezone('Asia/Baghdad')
GEMINI = "AIzaSyA5pzOpKVcMGm6Aek82KoB3Pk94dYg3LX4"
genai.configure(api_key=GEMINI)
model = genai.GenerativeModel("gemini-1.5-flash")
@ABH.on(events.NewMessage(pattern=r'(ترجمة|ترجمه)'))
async def translation(event):
    translator = Translator()
    if event.is_reply:
        replied_message = await event.get_reply_message()
        original_text = replied_message.text 
    else:
        command_parts = event.message.text.split(' ', 1)
        original_text = command_parts[1] if len(command_parts) > 1 else None
    if not original_text:
        await event.reply("يرجى الرد على رسالة تحتوي على النص المراد ترجمته أو كتابة النص بجانب الأمر.")
        return
    detected_language = translator.detect(original_text)
    if detected_language.lang == "ar": 
        translated = translator.translate(original_text, dest="en")
    else: 
        translated = translator.translate(original_text, dest="ar")
    response = (
        f"اللغة المكتشفة: {detected_language.lang}\n"
        f"النص المترجم: `{translated.text}`"
    )
    await event.reply(response)
rights_translation = {
    "change_info": "تغيير معلومات المجموعة",
    "post_messages": "نشر الرسائل",
    "edit_messages": "تعديل الرسائل",
    "delete_messages": "حذف الرسائل",
    "ban_users": "حظر الأعضاء",
    "invite_users": "دعوة أعضاء",
    "pin_messages": "تثبيت الرسائل",
    "add_admins": "إضافة مشرفين",
    "manage_call": "إدارة المكالمات الصوتية",
    "anonymous": "الوضع المتخفي",
    "manage_topics": "إدارة المواضيع",
}
def translate_rights_lines(rights_obj):
    lines = []
    for key, name in rights_translation.items():
        status = getattr(rights_obj, key, False)
        emoji = "👍🏾" if status else "👎🏾"
        lines.append(f"{emoji} ⇜ {name}")
    return "\n".join(lines) if lines else "لا يوجد صلاحيات"
@ABH.on(events.NewMessage(pattern=r'^صلاحياته(?: (.+))?$'))
async def his_rights(event):
    try:
        chat = await event.get_input_chat()
        match = event.pattern_match.group(1)
        if match:
            target = match
        else:
            reply = await event.get_reply_message()
            if not reply:
                await event.reply("استخدم الرد على رسالة المستخدم أو أرسل معرفه بعد الأمر.")
                return
            target = reply.sender_id
        result = await ABH(GetParticipantRequest(channel=chat, participant=target))
        translated = translate_rights_lines(result.participant.admin_rights)
        await event.reply(f"صلاحياته\n{translated}")
    except Exception:
        await event.reply("لا يمكن عرض الصلاحيات.")
@ABH.on(events.NewMessage(pattern=r'^لقبه(?: (.+))?$'))
async def nickname_r(event):
    try:
        chat = await event.get_input_chat()
        match = event.pattern_match.group(1)
        if match:
            target = match
        else:
            reply = await event.get_reply_message()
            if not reply:
                await event.reply("استخدم الرد على رسالة المستخدم أو أرسل معرفه بعد الأمر.")
                return
            target = reply.sender_id
        result = await ABH(GetParticipantRequest(channel=chat, participant=target))
        participant = result.participant
        nickname = getattr(participant, 'rank', None) or "مشرف"
        await event.reply(f"لقبه ↞ {nickname}")
    except Exception:
        await event.reply("المستخدم ليس مشرفًا أو لا يمكن العثور عليه.")
