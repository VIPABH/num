from __init__ import ABH

abh = [
    "ها",
    "تفظل",
    "كول",
    "اسمعك",
    "شرايد",
    "خلصني",
    "https://t.me/VIPABH/1214",
    "https://t.me/VIPABH/1215"
]
@ABH.on(events.NewMessage(pattern=r'^مخفي$'))
async def reply(event):
    if event.is_reply:
        return
    vipabh = random.choice(abh)
    if vipabh.startswith("http"):
        await event.reply(file=vipabh)
    else:
        await event.reply(vipabh)
@ABH.on(events.NewMessage(pattern='ابن هاشم'))
async def reply_abh(event):
    if event.chat_id == -1001968219024:
        rl = random.randint(1222, 1241)
        url = f"https://t.me/VIPABH/{rl}"
        caption = "أبن هاشم (رض) مرات متواضع ،🌚 @K_4x1"
        button = [Button.url(text="الking", url="https://t.me/K_4x1")]
        await event.client.send_file(event.chat_id, url, caption=caption, reply_to=event.message.id, buttons=button)
    else:
        return
