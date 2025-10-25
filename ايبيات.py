from telethon import events
from ABH import ABH
import requests, datetime
def to_date(timestamp):
    if not timestamp:
        return "غير متوفر"
    return datetime.datetime.utcfromtimestamp(timestamp).strftime("%Y-%m-%d %H:%M")
def get_chess_profile(username):
    base = f"https://api.chess.com/pub/player/{username.lower()}"
    headers = {"User-Agent": "TelegramChessBot/1.0 (contact@example.com)"}
    profile = requests.get(base, headers=headers, timeout=10)
    if profile.status_code == 404:
        return None
    if profile.status_code != 200:
        return {"error": f"⚠️ خطأ في الاتصال: {profile.status_code}"}
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
    await event.respond(f"♟ جاري جلب معلومات اللاعب **{username}** ...")
    data = get_chess_profile(username)
    if not data:
        await event.respond("❌ لم يتم العثور على هذا المستخدم على Chess.com.")
        return
    if "error" in data:
        await event.respond(data["error"])
        return
    s = data.get("stats", {})
    def rating(mode):
        item = s.get(f"chess_{mode}")
        if not item:
            return "غير متوفر"
        last = item.get("last", {}).get("rating")
        best = item.get("best", {}).get("rating")
        if last and best:
            return f"{last} (Elo: {best})"
        elif last:
            return str(last)
        else:
            return "غير متوفر"
    def record(mode):
        item = s.get(f"chess_{mode}")
        if not item or "record" not in item:
            return "غير متوفر"
        rec = item["record"]
        wins = rec.get("win", 0)
        losses = rec.get("loss", 0)
        draws = rec.get("draw", 0)
        total = wins + losses + draws
        return f"{wins} فوز / {losses} خسارة / {draws} تعادل (المجموع: {total})"
    profile_text = (
        f"♟ **معلومات اللاعب Chess.com** ♟\n\n"
        f"👤 **الاسم:** {data.get('username', 'غير متوفر')}\n"
        f"🏆 **اللقب:** {data.get('title', 'بدون')}\n"
        f"🌍 **الدولة:** {data.get('country', '').split('/')[-1] if data.get('country') else 'غير معروف'}\n"
        f"📅 **تاريخ الانضمام:** {to_date(data.get('joined'))}\n"
        f"🕐 **آخر ظهور:** {to_date(data.get('last_online'))}\n\n"
        f"📊 **التصنيفات:**\n"
        f"⚡ Blitz: {rating('blitz')} — {record('blitz')}\n"
        f"🔥 Bullet: {rating('bullet')} — {record('bullet')}\n"
        f"⏱ Rapid: {rating('rapid')} — {record('rapid')}\n"
        f"🧩 Puzzle: {rating('puzzle')}\n"
        f"📬 Daily: {rating('daily')} — {record('daily')}\n\n"
        f"🔗 [الملف الشخصي على Chess.com]({data.get('url')})"
    )
    await event.reply(profile_text, link_preview=False)
