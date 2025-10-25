from telethon import events
from Program import *
from ABH import ABH
import requests, datetime
def to_date(timestamp):
    if not timestamp: return "غير متوفر"
    return datetime.datetime.utcfromtimestamp(timestamp).strftime("%Y-%m-%d %H:%M")
def get_chess_profile(username):
    base = f"https://api.chess.com/pub/player/{username.lower()}"
    headers = {"User-Agent": "TelegramChessBot/1.0 (contact@example.com)"}
    profile = requests.get(base, headers=headers, timeout=10)
    if profile.status_code == 404: return None
    if profile.status_code != 200: return {"error": f"⚠️ خطأ في الاتصال: {profile.status_code}"}
    stats = requests.get(f"{base}/stats", headers=headers, timeout=10)
    stats_data = stats.json() if stats.status_code == 200 else {}
    data = profile.json()
    data["stats"] = stats_data
    return data
@ABH.on(events.NewMessage(pattern=r"^شطرنج\s+(\w+)$"))
async def save_chess_user(event):
    username = event.pattern_match.group(1)
    user_id = str(event.sender_id)
    r.set(f"chess_user:{user_id}", username)
    await event.reply(f"✅ تم تعيين اسمك في شطرنج.com إلى **{username}**.\nالآن يمكنك استخدام الأمر `الايلو` لمعرفة تصنيفك.")
@ABH.on(events.NewMessage(pattern=r"^الايلو(?:\s+(\w+))?$"))
async def get_elo(event):
    user_id = str(event.sender_id)
    username = event.pattern_match.group(1)
    if not username:
        stored_username = r.get(f"chess_user:{user_id}")
        if not stored_username:
            await event.respond("❌ لم يتم تعيين اسمك بعد.\nاكتب مثلًا:\n`شطرنج k_4x1`")
            return
        username = stored_username
    data = get_chess_profile(username)
    if not data:
        await event.respond("❌ لم يتم العثور على هذا المستخدم على Chess.com.")
        return
    if "error" in data:
        await event.respond(data["error"])
        return
    s = data.get("stats", {})
    item = s.get("chess_blitz")
    if not item or "record" not in item:
        wins = losses = draws = 0
        elo = "غير متوفر"
    else:
        rec = item["record"]
        wins = rec.get("win", 0)
        losses = rec.get("loss", 0)
        draws = rec.get("draw", 0)
        elo = item.get("last", {}).get("rating", "غير متوفر")
    profile_text = (
        f"الاسم -> {data.get('username','غير متوفر')}\n"
        f"الانشاء -> {to_date(data.get('joined'))}\n"
        f"اخر ظهور -> {to_date(data.get('last_online'))}\n"
        f"عدد الفوز -> {wins}\n"
        f"عدد الخسارات -> {losses}\n"
        f"عدد التعادلات -> {draws}\n"
        f"Blitz Elo -> {elo}"
    )
    await event.reply(profile_text, link_preview=False)
