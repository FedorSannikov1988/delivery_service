"""
The module is responsible for downloading/receiving data from the Telegram WebApp.
"""
from keyboards import AnswerQuestionChoicePaymentOrChangeDeliveryLocation, \
                      selection_for_registered_user
from db_api import update_delivery_address_in_database, \
                   update_payment_status_in_database, \
                   add_one_order_in_database, \
                   search_buyer_in_database, \
                   search_dish_in_database
from aiogram.fsm.context import FSMContext
from aiogram.types import PreCheckoutQuery, \
                          CallbackQuery, \
                          FSInputFile
from aiogram.utils.markdown import hbold
from loader import router_for_main_menu, \
                   bot
from states import NewDeliveryAddress
from config import TOKEN_FOR_UPAY
from datetime import timedelta, \
                     datetime
from aiogram import types, F
import json


ORDER_SAVING_TIME_MIN = 15


@router_for_main_menu.message(F.web_app_data)
async def web_app_data_entry(message: types.Message,
                             state: FSMContext,
                             search_result_buyer):
    """
    Getting data from WebApp Telegram.

    :param message: types.Message
    :param state: FSMContext
    :param search_result_buyer: Buyers
    :return: None
    """
    chat_id: int = message.chat.id
    id_telegram: int = message.from_user.id
    order_str: str = message.web_app_data.data
    order = json.loads(order_str)

    title_text: str = 'Ваш заказ:'
    await message.answer(text=title_text)

    total_cost_food: float = 0
    list_dishes_for_database: list = []

    for dish in order[:-1]:

        id_food = int(dish["id"][2:])
        number_servings = dish["count"]

        list_dishes_for_database.append({id_food: number_servings})

        dishes_from_database = \
            search_dish_in_database(id_food=id_food)

        title: str = dishes_from_database.name_food
        description: str = dishes_from_database.description_food
        picture: str = dishes_from_database.img_food
        price: float = dishes_from_database.price

        total_cost_food += price*number_servings

        photo = FSInputFile(path=picture)
        text = f'{hbold("Название: ")}' + title + '\n' + \
               f'{hbold("Описание: ")}' + description + '\n' + \
               f'{hbold("Цена за одну порцию: ")}' + str(price) + ' ₽' + '\n' + \
               f'{hbold("Количество порций: ")}' + str(number_servings)
        args_for_send_photo = {
            'photo': photo,
            'caption': text,
            'chat_id': chat_id
        }
        await bot.send_photo(**args_for_send_photo)

    delivery_information = order[len(order) - 1]
    full_cost: float = total_cost_food + delivery_information["shipping_cost"]

    text_full_cost_delivery_information_except_delivery_address: str = \
        f'Стоимость еды: {total_cost_food} ₽\n' \
        f'Стоимость доставки: {delivery_information["shipping_cost"]} ₽\n' \
        f'Полная стоимость: {full_cost} ₽\n' \
        f'Дата доставки: {delivery_information["delivery_date"]} \n' \
        f'Время доставки: {delivery_information["delivery_time"]} \n'
    await message.answer(text=
                         text_full_cost_delivery_information_except_delivery_address)

    if search_result_buyer:

        delivery_address: str = \
            search_result_buyer.default_adder_for_delivery

        text_delivery_address: str = \
            'Адресс доставки: ' + delivery_address
        await message.answer(text=text_delivery_address)

        list_dishes = json.dumps(list_dishes_for_database)

        cost_delivery: float = float(delivery_information["shipping_cost"])

        add_one_order_in_database(id_telegram=id_telegram,
                                  list_dishes=list_dishes,
                                  cost_food=total_cost_food,
                                  cost_delivery=cost_delivery,
                                  full_cost=full_cost,
                                  delivery_date=delivery_information["delivery_date"],
                                  delivery_time=delivery_information["delivery_time"],
                                  delivery_address=delivery_address)

        text: str = 'Выберите действие: \n' \
                    'Реквизиты для тестовой оплаты '\
                    '(что бы тестировщик проекта что-то ' \
                    'смог купить если сумма покупки не ' \
                    'более 1000 ₽) \n' \
                    'Номер карты: 1111 1111 1111 1026 \n' \
                    'Месяц/Год: 12/22 \n' \
                    'CVC: 000'
        await message.answer(text=text,
                             reply_markup=
                             selection_for_registered_user())

    else:

        order.append({'time_of_order_receipt': datetime.now()})
        await state.update_data({'order': order})

        text: str = f'Вам необходимо пройти регистрацию ' \
                    f'для чего нужно нажать кнопку: ' \
                    f'Зарегестрироваться. \n ' \
                    f'Если Вы пройдете регистрацию за ' \
                    f'{ORDER_SAVING_TIME_MIN} минут ' \
                    f'сможете оплатить сделанный ранее заказ.'
        await message.answer(text=text)


async def processing_order_after_registration(message: types.Message,
                                              state: FSMContext):
    """
    To process data received from the WebApp immediately after
    user registration. This function is called in the buyer_registration
    module if the user is not registered but has placed an order.

    :param message: types.Message
    :param state: FSMContext
    :return: None
    """

    fsm_context: dict = await state.get_data()

    order = fsm_context['order']

    time_of_order_receipt = order.pop()['time_of_order_receipt']

    for_comparison = \
        time_of_order_receipt + timedelta(minutes=
                                          ORDER_SAVING_TIME_MIN)

    if for_comparison >= datetime.now():

        chat_id = message.chat.id
        id_telegram = message.chat.id

        search_result_buyer = \
            search_buyer_in_database(id_telegram=id_telegram)

        title_text: str = 'Ваш заказ:'
        await message.answer(text=title_text)

        total_cost_food: float = 0
        list_dishes_for_database: list = []

        for dish in order[:-1]:
            id_food = int(dish["id"][2:])
            number_servings = dish["count"]

            list_dishes_for_database.append({id_food: number_servings})

            dishes_from_database = \
                search_dish_in_database(id_food=
                                        id_food)

            title: str = dishes_from_database.name_food
            description: str = dishes_from_database.description_food
            picture: str = dishes_from_database.img_food
            price: float = dishes_from_database.price

            total_cost_food += price * number_servings

            photo = FSInputFile(path=picture)
            text = f'{hbold("Название: ")}' + title + '\n' + \
                   f'{hbold("Описание: ")}' + description + '\n' + \
                   f'{hbold("Цена за одну порцию: ")}' + str(price) + ' ₽' + '\n' + \
                   f'{hbold("Количество порций: ")}' + str(number_servings)
            args_for_send_photo = {
                'photo': photo,
                'caption': text,
                'chat_id': chat_id
            }
            await bot.send_photo(**args_for_send_photo)

        delivery_information = order[len(order) - 1]
        full_cost: float = total_cost_food + delivery_information["shipping_cost"]

        text_full_cost_delivery_information_except_delivery_address: str = \
            f'Стоимость еды: {total_cost_food} ₽\n' \
            f'Стоимость доставки: {delivery_information["shipping_cost"]} ₽\n' \
            f'Полная стоимость: {full_cost} ₽\n' \
            f'Дата доставки: {delivery_information["delivery_date"]} \n' \
            f'Время доставки: {delivery_information["delivery_time"]} \n'
        await message.answer(text=
                             text_full_cost_delivery_information_except_delivery_address)

        delivery_address: str = \
            search_result_buyer.default_adder_for_delivery

        text_delivery_address: str = \
            'Адресс доставки: ' + delivery_address
        await message.answer(text=text_delivery_address)

        list_dishes = json.dumps(list_dishes_for_database)

        cost_delivery: float = float(delivery_information["shipping_cost"])

        add_one_order_in_database(id_telegram=id_telegram,
                                  list_dishes=list_dishes,
                                  cost_food=total_cost_food,
                                  cost_delivery=cost_delivery,
                                  full_cost=full_cost,
                                  delivery_date=delivery_information["delivery_date"],
                                  delivery_time=delivery_information["delivery_time"],
                                  delivery_address=delivery_address)

        text: str = 'Выберите действие: \n' \
                    'Реквизиты для тестовой оплаты ' \
                    '(если сумма покупки не более 1000 ₽) \n' \
                    'Номер карты: 1111 1111 1111 1026 \n' \
                    'Месяц/Год: 12/22 \n' \
                    'CVC: 000'
        await message.answer(text=text,
                             reply_markup=
                             selection_for_registered_user())

    else:
        text: str = f'Вы не прошли регистрацию за ' \
                    f'отведенные {ORDER_SAVING_TIME_MIN} ' \
                    f'минут.'
        await message.answer(text=text)


@router_for_main_menu.callback_query(AnswerQuestionChoicePaymentOrChangeDeliveryLocation.filter(
                                     F.payment_or_change_delivery_location ==
                                     "change_delivery_location"))
async def entering_new_delivery_address(callback: CallbackQuery,
                                        state: FSMContext):
    """
    Event processing (the button is pressed) change the
    delivery address.

    :param callback: CallbackQuery
    :param state: FSMContext
    :return: None
    """

    chat_id: int = callback.message.chat.id
    message_id: int = callback.message.message_id

    await bot.delete_message(chat_id=chat_id,
                             message_id=message_id)

    text: str = 'Введите новый адрес доставки:'
    args_for_send_message = {
        'text': text,
        'chat_id': chat_id
    }
    await bot.send_message(**args_for_send_message)

    await state.set_state(NewDeliveryAddress.wait_new_delivery_address)


@router_for_main_menu.message(NewDeliveryAddress.wait_new_delivery_address)
async def select_action_new_address_or_payment(message: types.Message,
                                               state: FSMContext,
                                               last_order_buyer):
    """
    Getting a new delivery address.

    :param message:types.Message
    :param state: FSMContext
    :param last_order_buyer: Orders
    :return: None
    """
    await state.set_state()

    new_delivery_address: str = message.text

    id_last_order_buyer: int = last_order_buyer.id_order

    try:
        update_delivery_address_in_database(id_order=
                                            id_last_order_buyer,
                                            new_delivery_address=
                                            new_delivery_address)

        text: str = "Адрес доставки изминен."

    except Exception:

        text: str = "Адрес доставки изменить не получилось."

    await message.answer(text=text + "\n" + "Выберите действие:",
                         reply_markup=selection_for_registered_user())


@router_for_main_menu.callback_query(AnswerQuestionChoicePaymentOrChangeDeliveryLocation.filter(
                                     F.payment_or_change_delivery_location == "pay"))
async def start_payment(callback: CallbackQuery,
                        last_order_buyer):
    """
    Event processing (the button is pressed) pay.

    :param callback: CallbackQuery
    :param last_order_buyer: Orders
    :return: None
    """
    full_cost_for_description: float = last_order_buyer.full_cost

    full_cost = full_cost_for_description * 100

    await bot.send_invoice(chat_id=callback.from_user.id,
                           title="Оплата готовой еды из "
                                 "службы доставки",
                           description=f"Оплата заказа на "
                                       f"{full_cost_for_description} "
                                       f"Рублей",
                           payload='pay_money',
                           provider_token=TOKEN_FOR_UPAY,
                           currency="Rub",
                           start_parameter="pay_money",
                           prices=[{
                               "label": "Rub",
                               "amount": full_cost
                           }])


@router_for_main_menu.pre_checkout_query()
async def pre_checkout_query(pre_checkout_query: PreCheckoutQuery):
    await bot.answer_pre_checkout_query(pre_checkout_query.id, ok=True)


@router_for_main_menu.message(F.successful_payment)
async def successful_payment(message: types.Message,
                             last_order_buyer):
    """
    Processing the successful payment event.

    :param message: types.Message
    :param last_order_buyer: Orders
    :return: None
    """

    id_last_order_buyer: int = last_order_buyer.id_order

    update_payment_status_in_database(id_order=id_last_order_buyer,
                                      payment_status=True)

    text = 'Ваш заказ оплачен. ' \
           'С Вами свяжутся для ' \
           'подтверждения (валидация ' \
           'заказа оператором).'
    await message.answer(text=text)
