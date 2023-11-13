"""
Start app/bot.
"""
from middlewares import BuyerSearchWhenReceivingDataFromWebApp,\
                        BuyerSearchDuringRegistration, \
                        LastOrderBuyerStartPayment, \
                        SuccessfulPaymentBuyer, \
                        SelectActionNewAddres, \
                        NumberOrdersBuyer, \
                        GetAllOrders, \
                        BookReviews
from handlers import router_for_main_menu
from loader import bot, dp
import asyncio


async def main() -> None:
    """
    Launching the application .

    :return: None
    """

    """
    Since there is only one menu, only one router was used.

    However, the reaction to each button/command was placed in a 
    separate module for ease of writing (since some chains of 
    events turned out to be too long for their adequate perception 
    in one file).
    """
    router_for_main_menu.message.middleware(BuyerSearchWhenReceivingDataFromWebApp())
    router_for_main_menu.callback_query.middleware(LastOrderBuyerStartPayment())
    router_for_main_menu.message.middleware(BuyerSearchDuringRegistration())
    router_for_main_menu.message.middleware(SuccessfulPaymentBuyer())
    router_for_main_menu.message.middleware(SelectActionNewAddres())
    router_for_main_menu.message.middleware(NumberOrdersBuyer())
    router_for_main_menu.message.middleware(GetAllOrders())
    router_for_main_menu.message.middleware(BookReviews())
    dp.include_router(router_for_main_menu)
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())
