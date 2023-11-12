"""
Starting (getting started) with a telegram bot.
"""
from aiogram.types import ReplyKeyboardRemove
from loader import router_for_main_menu
from aiogram.filters import Command
from aiogram import types, F


@router_for_main_menu.message(Command("hide_menu"))
@router_for_main_menu.message(F.text == "Скрыть меню")
async def close_menu(message: types.Message):
    """
    Reaction to the text "Hide menu".

    :param message: types.Message
    :return: None
    """

    text: str = \
        "Для вызова меню воспользуйтесь командой /start"
    await message.answer(text=text,
                         reply_markup=ReplyKeyboardRemove())
