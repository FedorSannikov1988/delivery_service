"""
Starting (getting started) with a telegram bot.
"""
from aiogram.utils.markdown import hunderline, \
                                   hlink, \
                                   hbold
from loader import router_for_main_menu
from keyboards import main_keyboard
from aiogram.filters import Command
from aiogram import types, F


@router_for_main_menu.message(Command("start"))
@router_for_main_menu.message(F.text == "Старт")
async def start_main_menu(message: types.Message):
    """
    Response to the start command.

    :param message: types.Message
    :param state: FSMContext
    :return: None
    """

    text: str = f'Здраствуйте, ' \
                f'{hbold(message.from_user.first_name)}! '\
                f'Это {hunderline("ПЕДПРОЕКТ")} !\n'\
                f'Добро пожаловать в службу доставки готовой еды! ' \
                f'В меню представлены блюда которые можно ' \
                f'{hunderline("купить и оформить доставку")} ! ' \
                f'Мой ➡️ ' \
                f'{hlink( url= r"https://t.me/Fedor_Sannikov", title="создатель")}.\n\n'
    await message.answer(text=text,
                         reply_markup=main_keyboard)
