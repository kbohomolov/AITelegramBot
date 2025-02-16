from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


inline_start_dialog_with_ai_keyboard = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='🏠 Повернутись до головного меню', callback_data='user_redirect_to_main_menu')]
])

inline_faq_questions_keyboard = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='🏠 Повернутись до головного меню', callback_data='user_redirect_to_main_menu')]
])

inline_settings_keyboard = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='👤 Мій профіль', callback_data='user_check_profile')],
    [InlineKeyboardButton(text='🤖 Обрати/Змінити AI - мовну модель', callback_data='change_ai_model')],
    [InlineKeyboardButton(text='🌎 Змінити мову інтерфейсу', callback_data='change_language')],
    [InlineKeyboardButton(text='🏠 Повернутись до головного меню', callback_data='user_redirect_to_main_menu')]
])

inline_user_profile_keyboard = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='↩️ Повернутись до попереднього меню', callback_data='user_redirect_to_settings_menu')],
    [InlineKeyboardButton(text='🏠 Повернутись до головного меню', callback_data='user_redirect_to_main_menu')]
])

inline_change_ai_model_keyboard = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='1️⃣ OpenAI', callback_data='user_select_openai_ai_model'),
    InlineKeyboardButton(text='2️⃣ Mistral AI', callback_data='user_select_mistral_ai_model'),
    InlineKeyboardButton(text='3️⃣ Claude Sonnet', callback_data='user_select_claude_sonnet')],
    [InlineKeyboardButton(text='↩️ Повернутись до попереднього меню', callback_data='user_redirect_to_settings_menu')],
    [InlineKeyboardButton(text='🏠 Повернутись до головного меню', callback_data='user_redirect_to_main_menu')]
])

inline_change_language_keyboard = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='🇺🇦 Українська', callback_data='user_select_ukrainian_language'),
    InlineKeyboardButton(text='🇬🇧 Англійська', callback_data='user_select_english_language')],
    [InlineKeyboardButton(text='↩️ Повернутись до попереднього меню', callback_data='user_redirect_to_settings_menu')],
    [InlineKeyboardButton(text='🏠 Повернутись до головного меню', callback_data='user_redirect_to_main_menu')]
])