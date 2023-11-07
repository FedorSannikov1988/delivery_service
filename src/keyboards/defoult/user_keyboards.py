"""
Creating a starting (main) keyboard
"""
from aiogram.types import ReplyKeyboardMarkup, \
                          KeyboardButton, \
                          WebAppInfo

path_web_url = WebAppInfo(url="https://fedorsannikov1988.github.io/")

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
                KeyboardButton(text="Регистрация",
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
