"""
Start app/bot
"""
from handlers import router_for_main_menu
from loader import bot, dp
import asyncio


async def main() -> None:
    """
    launching the application .

    :return: None
    """
    dp.include_router(router_for_main_menu)
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())
