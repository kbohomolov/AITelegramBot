from aiogram import F, Router, types
from aiogram.filters import Command, CommandStart
from aiogram.types import Message

from app.keyboards.reply_keyboard import main_keyboard


user_router = Router()

@user_router.message(CommandStart)
async def start_command(message: types.Message):
    await message.answer(f'Привіт, {message.from_user.full_name}!', reply_markup=main_keyboard)

@user_router.message(Command('help'))
async def help_command(message: types.Message):
    await message.answer('Тут допомога')