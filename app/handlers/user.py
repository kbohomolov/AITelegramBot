from aiogram import F, Router
from aiogram.filters import CommandStart
from aiogram.types import Message, CallbackQuery
from aiogram.exceptions import TelegramBadRequest
from functools import wraps
from aiogram.utils.i18n import gettext as _
from sqlalchemy.future import select
from app.database.models import async_session, KnowledgeBase
from app.services.ai_service import get_ai_response

import app.keyboards.inline_keyboard as inline_kb
import app.database.requests as rq

user_router = Router()

def check_active_user(handler):
    @wraps(handler)
    async def wrapper(event, *args, **kwargs):
        telegram_id = event.from_user.id
        user = await rq.get_user(telegram_id)

        if not user or not user.is_active:
            text = _("account_deleted", locale=kwargs.get("locale"))
            if isinstance(event, Message):
                await event.answer(text)
            elif isinstance(event, CallbackQuery):
                await event.answer(text, show_alert=True)
            return

        return await handler(event, *args, **kwargs)

    return wrapper

async def send_main_menu(event: Message | CallbackQuery, user_full_name: str, locale: str):
    text = _("main_menu_text", locale=locale).format(name=user_full_name)
    if isinstance(event, Message):
        await event.answer(text, reply_markup=inline_kb.main_menu(locale))
    else:
        await event.message.edit_text(text, reply_markup=inline_kb.main_menu(locale))

async def send_faq_menu(event: Message | CallbackQuery, locale: str):
    text = _("faq_text", locale=locale).format(name=event.from_user.full_name)
    if isinstance(event, CallbackQuery):
        await event.message.edit_text(text, reply_markup=inline_kb.faq_menu(locale))
    else:
        await event.answer(text, reply_markup=inline_kb.faq_menu(locale))

async def send_settings_menu(event: Message | CallbackQuery, locale: str):
    text = _("settings_text", locale=locale)
    if isinstance(event, CallbackQuery):
        await event.message.edit_text(text, reply_markup=inline_kb.settings_menu(locale))
    else:
        await event.answer(text, reply_markup=inline_kb.settings_menu(locale))

async def send_user_profile(event: Message | CallbackQuery, locale: str):
    user_info = await rq.get_user(event.from_user.id)
    registration_date = user_info.registration_date.strftime("%d.%m.%Y %H:%M:%S")

    role = _("role_admin", locale=locale) if user_info.is_admin else _("role_user", locale=locale)
    language = _("ukrainian", locale=locale) if user_info.language == "uk" else _("english", locale=locale)

    text = _("profile_text", locale=locale).format(
        id=user_info.id,
        date=registration_date,
        role=role,
        model="GPT-4o-mini",
        language=language
    )

    markup = inline_kb.user_profile(locale)

    if isinstance(event, Message):
        await event.answer(text, reply_markup=markup, parse_mode="HTML")
    else:
        current_text = event.message.text
        current_markup = event.message.reply_markup
        if current_text != text or current_markup != markup:
            try:
                await event.message.edit_text(text, reply_markup=markup, parse_mode="HTML")
            except TelegramBadRequest as e:
                if "message is not modified" not in str(e):
                    raise

async def send_language_menu(callback: CallbackQuery, locale: str):
    lang_name = _("ukrainian", locale=locale) if locale == "uk" else _("english", locale=locale)

    text = _("language_current", locale=locale).format(language=lang_name)

    await callback.message.edit_text(
        text,
        reply_markup=inline_kb.language_menu(locale),
        parse_mode="HTML"
    )

@user_router.message(CommandStart())
async def start_command(message: Message, locale):
    user = await rq.get_user(message.from_user.id)

    if user:
        if not user.is_active:
            await rq.activate_user(message.from_user.id)
    else:
        await rq.add_user(
            message.from_user.id,
            message.from_user.username,
            registration_date=message.date,
            is_admin=False
        )
        user = await rq.get_user(message.from_user.id)

    if user and user.is_admin:
        await message.answer(
            _("admin_welcome", locale=locale).format(name=message.from_user.full_name)
        )
    else:
        await send_main_menu(message, message.from_user.full_name, locale)

last_ai_messages: dict[int, int] = {}

@user_router.message(F.text == "🤖 Почати діалог зі ШІ")
@check_active_user
async def reply_start_ai(message: Message, locale):
    sent_msg = await message.answer(
        _("enter_request", locale=locale),
        reply_markup=inline_kb.start_ai_menu(locale)
    )
    last_ai_messages[message.from_user.id] = sent_msg.message_id

@user_router.message()
@check_active_user
async def handle_user_query(message: Message, locale):
    user_id = message.from_user.id
    start_msg_id = last_ai_messages.pop(user_id, None)
    if start_msg_id:
        try:
            await message.bot.delete_message(
                chat_id=message.chat.id,
                message_id=start_msg_id
            )
        except TelegramBadRequest:
            pass

    user_query = message.text.strip()

    await message.bot.send_chat_action(
        chat_id=message.chat.id,
        action="typing"
    )

    async with async_session() as session:
        result = await session.execute(
            select(KnowledgeBase).where(
                KnowledgeBase.question.ilike(f"%{user_query.lower()}%")
            )
        )
        kb_item = result.scalars().first()

    if kb_item:
        answer = kb_item.answer
    else:
        answer = await get_ai_response(user_query, locale)
    try:
        await message.reply(
            answer,
            reply_markup=inline_kb.end_dialog_menu(locale),
            parse_mode="Markdown"
        )
    except Exception:
        await message.reply(
            answer,
            reply_markup=inline_kb.end_dialog_menu(locale)
        )

@user_router.callback_query(F.data == "end_ai_dialog")
@check_active_user
async def end_ai_dialog(callback: CallbackQuery, locale: str):
    if callback.from_user.id in last_ai_messages:
        del last_ai_messages[callback.from_user.id]

    await callback.message.edit_text(
        _("dialog_ended", locale=locale),
        reply_markup=inline_kb.main_menu(locale)
    )

@user_router.message(F.text == "⁉️ FAQ")
@check_active_user
async def reply_open_faq(message: Message, locale):
    await send_faq_menu(message, locale)

@user_router.message(F.text == "⚙️ Налаштування")
@check_active_user
async def reply_open_settings(message: Message, locale):
    await send_settings_menu(message, locale)

@user_router.callback_query(F.data == "menu_start_ai")
@check_active_user
async def start_ai(callback: CallbackQuery, locale):
    await callback.message.edit_text(
        _("enter_request", locale=locale),
        reply_markup=inline_kb.start_ai_menu(locale)
    )
    last_ai_messages[callback.from_user.id] = callback.message.message_id

@user_router.callback_query(F.data == "menu_faq")
@check_active_user
async def open_faq(callback: CallbackQuery, locale):
    await send_faq_menu(callback, locale)

@user_router.callback_query(F.data == "menu_settings")
@check_active_user
async def open_settings(callback: CallbackQuery, locale):
    await send_settings_menu(callback, locale)

@user_router.callback_query(F.data == "faq_examples")
@check_active_user
async def faq_examples(callback: CallbackQuery, locale):
    await callback.message.edit_text(
        _("faq_examples_text", locale=locale),
        reply_markup=inline_kb.faq_examples(locale)
    )

@user_router.callback_query(F.data == "faq_usage_bot")
@check_active_user
async def faq_usage(callback: CallbackQuery, locale):
    await callback.message.edit_text(
        _("faq_usage_text", locale=locale),
        reply_markup=inline_kb.faq_usage(locale)
    )

@user_router.callback_query(F.data == "user_check_profile")
@check_active_user
async def user_check_profile(callback: CallbackQuery, locale):
    await send_user_profile(callback, locale)

@user_router.callback_query(F.data == "user_delete_account")
@check_active_user
async def delete_account(callback: CallbackQuery, locale):
    await callback.message.edit_text(
        _("delete_confirm", locale=locale),
        reply_markup=inline_kb.confirm_delete_menu(locale),
        parse_mode="HTML"
    )

@user_router.callback_query(F.data == "confirm_delete_account")
@check_active_user
async def confirm_delete(callback: CallbackQuery, locale):
    await rq.deactivate_user(callback.from_user.id)
    await callback.message.edit_text(
        _("delete_success", locale=locale),
        parse_mode="HTML"
    )

@user_router.callback_query(F.data == "cancel_delete_account")
@check_active_user
async def cancel_delete(callback: CallbackQuery, locale):
    await send_user_profile(callback, locale)

@user_router.callback_query(F.data == "change_language")
@check_active_user
async def change_language(callback: CallbackQuery, locale):
    await send_language_menu(callback, locale)

@user_router.callback_query(F.data == "user_select_uk")
@check_active_user
async def select_uk(callback: CallbackQuery):
    await rq.update_user_language(callback.from_user.id, "uk")

    await send_language_menu(callback, locale="uk")
    await callback.answer()

@user_router.callback_query(F.data == "user_select_en")
@check_active_user
async def select_en(callback: CallbackQuery):
    await rq.update_user_language(callback.from_user.id, "en")

    await send_language_menu(callback, locale="en")
    await callback.answer()

@user_router.callback_query(F.data == "user_redirect_to_main_menu")
@check_active_user
async def back_to_main(callback: CallbackQuery, locale):
    await send_main_menu(callback, callback.from_user.full_name, locale)

@user_router.callback_query(F.data == "user_redirect_to_settings_menu")
@check_active_user
async def back_to_settings(callback: CallbackQuery, locale):
    await send_settings_menu(callback, locale)

@user_router.callback_query(F.data == "user_redirect_to_faq_menu")
@check_active_user
async def back_to_faq(callback: CallbackQuery, locale):
    await send_faq_menu(callback, locale)
