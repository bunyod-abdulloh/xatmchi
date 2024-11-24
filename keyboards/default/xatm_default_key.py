from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

menu = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)

menu.insert(KeyboardButton("📖 Қоида ва йўриқнома"))
menu.insert(KeyboardButton("✅ Иштирок этиш"))
menu.add(KeyboardButton("♻ Қайтариш"))
menu.insert(KeyboardButton("👤 ID олиш"))
menu.add(KeyboardButton("⬅️ Ortga"))

xatm_adminka = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)

xatm_adminka.insert(KeyboardButton("📊 Жорий ҳолат"))
xatm_adminka.add(KeyboardButton("🔓 Хатм вақтини очиш"))
xatm_adminka.insert(KeyboardButton("🔒 Хатм вақтини ёпиш"))
xatm_adminka.add(KeyboardButton("🧮 Сарҳисоб"))
xatm_adminka.insert(KeyboardButton("❎ Қайтариш админ"))
xatm_adminka.add(KeyboardButton("🏡 Bosh sahifa"))
