from telethon import events 
from addanddel import *
from Resources import *
from Program import *
from guard import *
from count import *
from games import *
from group import *
from other import *
from ABH import *
from امسح import *
@ABH.on(events.NewMessage(incoming=True))
async def litsin_to_all_incoming(e):
  await store_media_messages(e)
@ABH.on(events.NewMessage)
async def litsin_to_all(e):
  await check_math_answer(e)
  await monitor_messages(e)
  await unified_handler(e)
  # await answer_handler(e)
  # await unified_handler(e)
  await faster_result(e)
  await guess_number(e)
  await check_quist(e)
  await check_sport(e)
  await som(e)
  await top(e)
  m = e.message
  text = e.text
  msg_type = get_message_type(m)
  await info(e, msg_type)
  if text in ('معلوماتي', 'معلومات', 'احصائياتي'):
      user_stats = await info(e, None)
      stats_str = "\n".join(
          f"◉ {k}: {v}"
          for k, v in user_stats.items())
      await e.reply(f"📊 إحصائياتك الحالية:\n\n{stats_str}")
  elif text in ('احصائياته', 'معلوماته'):
      x = await e.get_reply_message()
      if x:
          user_stats = await info(x, None)
          stats_str = "\n".join(
              f"◉ {k}: {v}"
              for k, v in user_stats.items())
          await e.reply(f"📊 {e.text}:\n\n{stats_str}")
  elif text == 'حافر':
    await e.reply("[حيثُ الجمال](https://t.me/x04ou)")
@ABH.on(events.CallbackQuery)
async def litson(e):
  await promoti(e)
  await callback_handler(e)
  await callbacklist(e)
  data = e.data.decode('utf-8') if isinstance(e.data, bytes) else e.data
  if data == "new_math":
    await new_math(e)
  elif data == 'ignore_math':
    await ignore_math(e)
  elif data == 'moneymuch':
    await show_money(e)
  elif data=='startGame':
      await handle_rings(e)
  elif data=='startx':
    await start_game(e)
@ABH.on(events.InlineQuery)
async def litsonINLIN(e):
  await inlineupdate(e)
