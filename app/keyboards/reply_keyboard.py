from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


main_admin_keyboard = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text='🤖 Почати діалог зі ШІ'),  KeyboardButton(text='⁉️ FAQ (Поширені питання)')],
    [KeyboardButton(text='⚙️ Налаштування'), KeyboardButton(text='🔐 Панель адміністратора')],
],  resize_keyboard=True)

main_user_keyboard = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text='🤖 Почати діалог зі ШІ'),  KeyboardButton(text='⁉️ FAQ (Поширені питання)')],
    [KeyboardButton(text='⚙️ Налаштування')],
],  resize_keyboard=True)
