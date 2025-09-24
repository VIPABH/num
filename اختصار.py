import os, re, json, inspect, importlib
from telethon import events
from ABH import ABH
OUTPUT_FILE = "shortcuts.json"
shortcuts = {}
COMMANDS = {}
for file in os.listdir("."):
    if file.endswith(".py") and file != os.path.basename(__file__):
        module_name = file[:-3]
        print(f"جارٍ استيراد الوحدة: {module_name}")
        try:
            module = importlib.import_module(module_name)
            print(f"تم استيراد الوحدة: {module_name}")
        except Exception as e:
            print(f"❌ فشل استيراد {file}: {e}")
            continue
        for name, obj in inspect.getmembers(module, inspect.iscoroutinefunction):
            print(f"جارٍ فحص الدالة: {name}")
            if hasattr(obj, "_events"):
                patterns = []
                for e in getattr(obj, "_events"):
                    print(f"جارٍ فحص الحدث: {e}")
                    if isinstance(e, events.NewMessage) and e.pattern:
                        patterns.append(str(e.pattern))
                        print(f"جارٍ إضافة الباترن: {e.pattern}")
                if patterns:
                    COMMANDS[name] = patterns
                    print(f"جارٍ إضافة الدالة: {name}")
with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
    json.dump(COMMANDS, f, ensure_ascii=False, indent=4)
print(f"✅ تم حفظ جميع الدوال والباترنات في {OUTPUT_FILE}")
@ABH.on(events.NewMessage(pattern=r"^اضف اختصار (.+?) (.+)$"))
async def add_shortcut_cmd(event):
    main, shortcut = event.pattern_match.group(1), event.pattern_match.group(2)
    if main not in COMMANDS:
        await event.reply(f"❌ لم يتم العثور على الدالة {main}")
        return
    if main not in shortcuts:
        shortcuts[main] = {}
    shortcuts[main][shortcut] = COMMANDS[main]["patterns"][0]
    save_shortcuts(shortcuts)
    await event.reply(f"✅ تم إضافة الاختصار `{shortcut}` للدالة `{main}`")
@ABH.on(events.NewMessage(pattern=r"^احذف اختصار (.+)$"))
async def remove_shortcut_cmd(event):
    s = event.pattern_match.group(1)
    found = False
    for func_name in shortcuts:
        if s in shortcuts[func_name]:
            del shortcuts[func_name][s]
            found = True
            break
    if found:
        save_shortcuts(shortcuts)
        await event.reply(f"✅ تم حذف الاختصار `{s}`")
    else:
        await event.reply(f"❌ لم يتم العثور على الاختصار `{s}`")
@ABH.on(events.NewMessage(pattern=r"^قائمة الاختصارات$"))
async def list_shortcuts_cmd(event):
    if not shortcuts:
        await event.reply("ℹ️ لا توجد اختصارات محفوظة.")
        return
    msg = "📂 قائمة الاختصارات:\n\n"
    for func_name, mapping in shortcuts.items():
        msg += f"🔹 {func_name}:\n"
        for new, old in mapping.items():
            msg += f"   `{new}` ➝ `{old}`\n"
    await event.reply(msg[:4000])
