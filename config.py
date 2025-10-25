from ABH import ABH, events, bot_token
from datetime import datetime
import os, json, pytz
from Resources import * 
from addanddel import * 
from Program import * 
from count import *
from games import * 
from group import * 
from guard import * 
from reply import * 
from other import * 
from اختصار import * 
from الايدي import * 
from mem import * 
from top import * 
from امسح import * 
from يوت import *
from المستمع import *
from ايبيات import *
baghdad_tz = pytz.timezone("Asia/Baghdad")
start_time = datetime.datetime.now(baghdad_tz)
@ABH.on(events.NewMessage(pattern='وقت التشغيل', from_users=[wfffp]))
async def timerun(event):
    now = datetime.now(baghdad_tz)
    diff = now - start_time
    days = diff.days
    hours = diff.seconds // 3600
    minutes = (diff.seconds % 3600) // 60
    duration_parts = []
    if days > 0:
        duration_parts.append(f"{days} يوم")
    if hours > 0:
        duration_parts.append(f"{hours} ساعة")
    if minutes > 0:
        duration_parts.append(f"{minutes} دقيقة")

    duration_text = " و ".join(duration_parts) if duration_parts else "أقل من دقيقة"
    start_str = start_time.strftime("%y/%m/%d--%I:%M%p")
    now_str = now.strftime("%y/%m/%d--%I:%M%p")
    message = (
        f"🕒 **بدأ التشغيل:** {start_str}\n"
        f"🕰️ **الوقت الحالي في بغداد:** {now_str}\n"
        f"⏳ **مدة التشغيل:** {duration_text}"
    )
    await event.reply(message)
def main():
    print(f'anymous is working at {hour} ✓')
    ABH.start(bot_token=bot_token)
    ABH.run_until_disconnected()
if __name__ == "__main__":
    main()
