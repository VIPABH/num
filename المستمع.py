from telethon import events 
from Resources import *
from Program import *
from count import *
from games import *
from group import *
from ABH import *
@ABH.on(events.NewMessage)
async def litsin_to_all(e):
  text = e.text
  await som(e)
  await unified_handler(e)
  await check_math_answer(e)
  await answer_handler(e)
  await check_quist(e)
  await check_sport(e)
  await faster_reult(e)
  await faster_reult(e)
  await monitor_messages(e)
  m = e.message
  msg_type = get_message_type(m)
  await info(e, msg_type)
  if text in ('معلوماتي', 'معلومات'):
      user_stats = await info(e, None)
      stats_str = "\n".join(
          f"{i+1} ⟶ {k} : {v}"
          for i, (k, v) in enumerate(user_stats.items())
      )
      await e.reply(f"📊 إحصائياتك الحالية:\n\n{stats_str}")
  elif text == 'معلوماته':
      x = await e.get_reply_message()
      if x:
          user_stats = await info(x, None)
          stats_str = "\n".join(
              f"{i+1} ⟶ {k} : {v}"
              for i, (k, v) in enumerate(user_stats.items())
          )
          await e.reply(f"📊 إحصائياته:\n\n{stats_str}")
@ABH.on(events.CallbackQuery)
async def litson(e):
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
