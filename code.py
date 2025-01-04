from telethon import TelegramClient, events
from telethon.tl.types import ChatBannedRights
import os
api_id = os.getenv('API_ID')      
api_hash = os.getenv('API_HASH')  
bot_token = os.getenv('BOT_TOKEN') 
client = TelegramClient('n', api_id, api_hash).start(bot_token=bot_token)
restricted_users = []
mutttof = []
unmute_permissions = ChatBannedRights(until_date=None, send_messages=None)
mute_permissions = ChatBannedRights(until_date=None, send_messages=False)
@client.on(events.NewMessage(pattern="المق"))
async def list_restricted_users(event):
    global restricted_users

    if not event.is_group:
        await event.reply("⌔ هذا الأمر يعمل فقط في المجموعات.")
        return

    response = "⌔ قائمة المقيدين:\n\n"
    updated_restricted_users = []

    for i, user_id in enumerate(restricted_users, 1):
        try:
            permissions = await client.get_permissions(event.chat_id, user_id)
            if not permissions.send_messages:
                updated_restricted_users.append(user_id)
                user = await client.get_entity(user_id)
                if user.username:
                    mention = f"[{user.first_name}](https://t.me/{user.username})"
                else:
                    mention = f"[{user.first_name}](tg://user?id={user.id})"
                response += f"{i}- {mention} ({user.id})\n"
            else:
                continue
        except Exception as e:
            response += f"{i}- [مستخدم مجهول](tg://user?id={user_id}) ({user_id})\n"

    restricted_users = updated_restricted_users

    if updated_restricted_users:
        await event.reply(response, parse_mode="md")
    else:
        await event.reply("⌔ لا يوجد أي مستخدمين مقيدين حاليًا.")

    



@client.on(events.NewMessage(pattern="تق"))
async def mute_user(event):
    global restricted_users

    if not event.is_group:
        await event.reply("⌔ هذا الأمر يعمل فقط في المجموعات.")
        return

    sender = await event.get_sender()
    user_status = await client.get_permissions(event.chat_id, sender.id)

    if user_status.is_admin or sender.id == 5089553588:
        if event.chat_id in mutttof:
            await event.reply("⌔ التقييد غير مفعل في هذه المجموعة.")
            return

        if not event.reply_to_msg_id:
            await event.reply("⌔ يجب الرد على رسالة المستخدم الذي تريد تقيده.")
            return

        reply_message = await event.get_reply_message()
        user_to_restrict = await client.get_entity(reply_message.sender_id)

        if user_to_restrict.id == 5089553588:
            await event.reply("⌔ عذرًا، لا يمكنك تقيد المطور.")
            return

        await client.edit_permissions(
            event.chat_id,
            user_to_restrict.id,
            send_messages=False
        )

        restricted_users.append(user_to_restrict.id)

        if user_to_restrict.username:
            mention = f"[@{user_to_restrict.username}](tg://user?id={user_to_restrict.id})"
        else:
            mention = f"[{user_to_restrict.first_name}](tg://user?id={user_to_restrict.id})"

        await event.reply(f"✅ ¦ تم تقيد المستخدم بنجاح: {mention}", parse_mode="md")
    else:
        await event.reply("⌔ ليس لديك صلاحيات لتنفيذ هذا الأمر.")


client.run_until_disconnected()
