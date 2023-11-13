"""
The module is responsible for receiving the operating instructions for this bot.
"""
from loader import router_for_main_menu
from aiogram.filters import Command
from aiogram import types, F
from loader import all_urls


@router_for_main_menu.message(Command("manual"))
@router_for_main_menu.message(F.text == "Инструкция")
async def give_all_commands_for_users(message: types.Message):
    """
    Loads all commands available to the user from the
    users_answers.json file uploaded to all_urls['manual_for_bot'].

    :param message: types.Message
    :return: None
    """

    url_gif_for_manual: str = all_urls['manual_for_bot']

    await message.answer_animation(animation=
                                   url_gif_for_manual)
