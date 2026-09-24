from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.i18n import gettext as _
from torch.distributed.tensor.parallel import style


def main_menu(locale: str) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=_("start_ai", locale=locale), style="primary", callback_data="menu_start_ai")],
        [InlineKeyboardButton(text=_("faq", locale=locale), style="primary", callback_data="menu_faq")],
        [InlineKeyboardButton(text=_("settings", locale=locale), style="primary", callback_data="menu_settings")]
    ])

def start_ai_menu(locale: str) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=_("back_main", locale=locale), style="primary", callback_data="user_redirect_to_main_menu")]
    ])

def faq_menu(locale: str) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=_("faq_examples", locale=locale), style="primary", callback_data="faq_examples")],
        [InlineKeyboardButton(text=_("faq_usage", locale=locale), style="primary", callback_data="faq_usage_bot")],
        [InlineKeyboardButton(text=_("back_main", locale=locale), style="primary", callback_data="user_redirect_to_main_menu")]
    ])

def faq_usage(locale: str) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=_("back", locale=locale), style="primary", callback_data="user_redirect_to_faq_menu")],
        [InlineKeyboardButton(text=_("back_main", locale=locale), style="primary", callback_data="user_redirect_to_main_menu")]
    ])

def faq_examples(locale: str) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=_("back", locale=locale), style="primary", callback_data="user_redirect_to_faq_menu")],
        [InlineKeyboardButton(text=_("back_main", locale=locale), style="primary", callback_data="user_redirect_to_main_menu")]
    ])

def settings_menu(locale: str) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=_("profile", locale=locale), style="primary", callback_data="user_check_profile")],
        [InlineKeyboardButton(text=_("change_lang", locale=locale), style="primary", callback_data="change_language")],
        [InlineKeyboardButton(text=_("back_main", locale=locale), style="primary", callback_data="user_redirect_to_main_menu")]
    ])

def user_profile(locale: str) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=_("delete_account", locale=locale), style="primary", callback_data="user_delete_account")],
        [InlineKeyboardButton(text=_("back", locale=locale), style="primary", callback_data="user_redirect_to_settings_menu")],
        [InlineKeyboardButton(text=_("back_main", locale=locale), style="primary", callback_data="user_redirect_to_main_menu")]
    ])

def confirm_delete_menu(locale: str) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=_("confirm_delete", locale=locale), style="success", callback_data="confirm_delete_account")],
        [InlineKeyboardButton(text=_("cancel", locale=locale), style="danger" , callback_data="cancel_delete_account")]
    ])

def language_menu(locale: str) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text=_("ukrainian", locale=locale), style="primary", callback_data="user_select_uk"),
            InlineKeyboardButton(text=_("english", locale=locale), style="primary", callback_data="user_select_en")
        ],
        [InlineKeyboardButton(text=_("back", locale=locale), style="primary", callback_data="user_redirect_to_settings_menu")],
        [InlineKeyboardButton(text=_("back_main", locale=locale), style="primary", callback_data="user_redirect_to_main_menu")]
    ])

def end_dialog_menu(locale: str) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=_("back_main", locale=locale), style="primary", callback_data="user_redirect_to_main_menu")]
    ])