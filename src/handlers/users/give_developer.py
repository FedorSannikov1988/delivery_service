"""
The module is responsible for obtaining the data of the
developer of this product.
"""
from loader import router_for_main_menu
from aiogram.filters import Command
from aiogram import types, F
from loader import all_urls


@router_for_main_menu.message(Command("developer"))
@router_for_main_menu.message(F.text == "Разработчик")
async def developer_bot(message: types.Message):
    """
    Says who developed the bot.

    :param message: types.Message
    :return: None
    """

    text: str = f"Данного бота разработал: \n" \
                f"{all_urls['link_developer_telegram']} \n" \
                f"{all_urls['link_developer_github']} \n" \
                f"{all_urls['link_developer_vk']} \n"
    await message.answer(text=text)
