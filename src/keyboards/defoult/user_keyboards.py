"""
Main keyboard.
"""
from aiogram.types import ReplyKeyboardMarkup, \
                          KeyboardButton, \
                          WebAppInfo
from config import URL_FOR_WEB_APP


path_web_url = WebAppInfo(url=URL_FOR_WEB_APP)


main_keyboard = \
    ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(text="Помощь"),
                KeyboardButton(text="Инструкция")
            ],
            [
                KeyboardButton(text="Меню готовых блюд",
                               web_app=path_web_url),
                KeyboardButton(text="Мои заказы"),
                KeyboardButton(text="Зарегестрироваться",
                               request_contact=True)
            ],
            [
                KeyboardButton(text="Книга отзывов"),
                KeyboardButton(text="Разработчик"),
                KeyboardButton(text="Скрыть меню"),
            ]
        ],
        resize_keyboard=True
    )
