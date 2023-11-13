"""
Starting (getting started) with a telegram bot.
"""
from aiogram.fsm.context import FSMContext
from loader import router_for_main_menu, \
                   bot
from states import EnteringNumberOrders
from aiogram.types import FSInputFile
from aiogram.filters import Command
from aiogram import types, F


@router_for_main_menu.message(Command("my_orders"))
@router_for_main_menu.message(F.text == "Мои заказы")
async def give_my_orders(message: types.Message,
                         number_orders_buyer: int,
                         state: FSMContext):

    if number_orders_buyer > 0:

        text: str = \
            "Вы сделали заказов: " + str(number_orders_buyer) + " ." \
            "Введите количество заказов начиная " \
            "с последнего сделанного Вами " \
            "информацию о которых хотите увидеть."

        await state.set_state(EnteringNumberOrders.wait_number_orders)

    else:

        text: str = \
            "Вы нечего не заказывали."

    await message.answer(text=text)


@router_for_main_menu.message(EnteringNumberOrders.wait_number_orders)
async def enter_number_orders(message: types.Message,
                              number_orders_buyer: int,
                              prepared_list_orders: list,
                              state: FSMContext):

    number_orders_str: str = message.text

    try:
        number_orders: int = int(number_orders_str)
        chat_id: int = message.chat.id

        if 0 < number_orders <= number_orders_buyer:

            for order in prepared_list_orders[0:number_orders]:

                title_order: str = \
                    f'Дата и время поступления заказа: ' + \
                    str(order['time_order_receipt'].strftime("%d.%m.%Y %H:%M")) + '\n' \
                    f'Стоимость еды: ' + \
                    str(order['cost_food']) + ' ₽\n' + \
                    f'Стоимость доставки: ' + \
                    str(order['cost_delivery']) + ' ₽\n' \
                    f'Полная стоимость заказа: ' + \
                    str(order['full_cost']) + ' ₽\n' \
                    f'Дата и время доставки: ' + \
                    str(order['date_and_time_delivery'].strftime("%d.%m.%Y %H:%M")) + '\n' \
                    f'Адрес доставки: ' + \
                    str(order['delivery_address']) + '\n' \
                    f'Статус оплаты: ' + \
                    f'{handler_for_true_false(data=order["payment_status"])}' + '\n' \
                    'Статус доставки: ' + \
                    f'{handler_for_true_false(data=order["delivery_status"])}' + '\n' \
                    f'Подробное описание содержания заказа:'
                await message.answer(text=title_order)

                for dishes in order['dishes']:
                    title_dish: str = \
                        'Название: ' + dishes['name_food'] + '\n' \
                        'Описание: ' + dishes['description_food'] + '\n' \
                        'Цена: ' + str(dishes['price']) + ' ₽\n' \
                        'Заказанное количество: ' + str(dishes['count']) + '\n'

                    photo = FSInputFile(path=dishes['img_food'])
                    args_for_send_photo = {
                        'photo': photo,
                        'caption': title_dish,
                        'chat_id': chat_id
                    }
                    await bot.send_photo(**args_for_send_photo)

            await state.set_state()

        else:
            text: str = \
                "Вы сделали заказов: " + str(number_orders_buyer) + " ." \
                "Введите количество заказов начиная " \
                "с последнего сделанного Вами " \
                "информацию о которых хотите увидеть."
            await message.answer(text=text)

    except ValueError:

        text: str = \
            "Вы сделали заказов: " + str(number_orders_buyer) + " ." \
            "Введите количество заказов начиная " \
            "с последнего сделанного Вами " \
            "информацию о которых хотите увидеть."
        await message.answer(text=text)


def handler_for_true_false(data: bool) -> str:

    if data:
        return 'Выполнено'
    else:
        return 'Не выполнено'
