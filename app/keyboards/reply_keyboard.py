from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


main_keyboard = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text='🤖 Почати діалог зі ШІ'),  KeyboardButton(text='⁉️ FAQ (Поширені питання)')],
    [KeyboardButton(text='⚙️ Налаштування'), KeyboardButton(text='🔐 Панель адміністратора')],
],  resize_keyboard=True)

#],  input_field_placeholder='Оберіть потрібний пункт з меню нижче:', resize_keyboard=True)