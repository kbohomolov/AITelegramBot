from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


inline_settings_keyboard = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='👤 Мій профіль', callback_data='user_check_profile')],
    [InlineKeyboardButton(text='🤖 Обрати/Змінити AI - мовну модель', callback_data='change_ai_model')],
    [InlineKeyboardButton(text='🌎 Змінити мову інтерфейсу', callback_data='change_language')],
    [InlineKeyboardButton(text='↩️ Повернутись до головного меню', callback_data='user_redirect_to_main_menu')]
])