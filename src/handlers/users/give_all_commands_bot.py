"""
The module is responsible for receiving all commands available to the user.
"""
from loader import router_for_main_menu
from loader import all_answer_for_user
from aiogram.filters import Command
from aiogram import types, F


@router_for_main_menu.message(Command("help"))
@router_for_main_menu.message(F.text == "Помощь")
async def give_all_commands_for_users(message: types.Message):
    """
    Response to the help command .
    Displays a list of all commands .

    :param message: types.Message
    :return: None
    """
    text: str = ''
    for command, description in \
            all_answer_for_user['all_commands_for_users'].items():
        text += command + ' - ' + description + '\n'
    await message.answer(text=text)
