"""
Loading data from database for handlers.
"""
from db_api import search_last_review_buyer_in_database, \
                   search_last_order_buyer_in_database, \
                   search_all_orders_buyer_in_database, \
                   search_buyer_in_database, \
                   search_dish_in_database
from aiogram.types import CallbackQuery, \
                          Message
from aiogram import BaseMiddleware
from typing import Awaitable, \
                   Callable, \
                   Dict, \
                   Any
import json


class NumberOrdersBuyer(BaseMiddleware):
    async def __call__(
            self,
            handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]],
            event: Message,
            data: Dict[str, Any]
    ) -> Any:
        """
        Outputs to the event handler the number of
        orders made by the registered user .

        :param handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]]
        :param event: Message
        :param data: Dict[str, Any]
        :return: int
        """
        text_or_command: str = event.text

        search_text_one: str = "Мои заказы"
        search_command_one: str = "/my_orders"

        if search_text_one == text_or_command or \
                search_command_one == text_or_command:

            id_telegram_buyer = event.from_user.id

            orders = \
                search_all_orders_buyer_in_database(id_telegram=
                                                    id_telegram_buyer)

            data["number_orders_buyer"] = len(orders)

        return await handler(event, data)


class SuccessfulPaymentBuyer(BaseMiddleware):
    async def __call__(
            self,
            handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]],
            event: Message,
            data: Dict[str, Any]
    ) -> Any:
        """
        Returns the last order of the buyer upon successful payment.

        :param handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]]
        :param event: Message
        :param data: Dict[str, Any]
        :return: Orders
        """
        if event.successful_payment:

            id_telegram_buyer: int = event.from_user.id

            search_result = \
                search_last_order_buyer_in_database(id_telegram=
                                                    id_telegram_buyer)

            data["last_order_buyer"] = search_result

        return await handler(event, data)


class BookReviews(BaseMiddleware):
    async def __call__(
            self,
            handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]],
            event: Message,
            data: Dict[str, Any]
    ) -> Any:
        """
        Returns the user's last review to the event handler (feedback book).

        :param handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]]
        :param event: Message
        :param data: Dict[str, Any]
        :return: BookReviews
        """
        text_or_command: str = event.text

        search_text_one: str = "Книга отзывов"
        search_command_one: str = "/reviews"

        if search_text_one == text_or_command or \
                search_command_one == text_or_command:

            id_telegram_buyer = event.from_user.id

            result_search_buyer = \
                search_buyer_in_database(id_telegram=
                                         id_telegram_buyer)

            data["result_search_buyer"] = result_search_buyer

            if result_search_buyer:

                last_review_buyer_from_db = \
                    search_last_review_buyer_in_database(id_telegram=
                                                         id_telegram_buyer)
            else:
                last_review_buyer_from_db = None

            data["last_review_buyer_from_db"] = last_review_buyer_from_db

        return await handler(event, data)


class BuyerSearchDuringRegistration(BaseMiddleware):
    async def __call__(
            self,
            handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]],
            event: Message,
            data: Dict[str, Any]
    ) -> Any:
        """
        Returns the buyer from the buyers table to the event handler
        after sending the user's contact (clicking the Register button).

        :param handler:  Callable[[Message, Dict[str, Any]], Awaitable[Any]]
        :param event: Message
        :param data: Dict[str, Any]
        :return: Buyers
        """

        if event.contact:

            id_telegram_buyer = event.from_user.id

            search_result = \
                search_buyer_in_database(id_telegram=
                                         id_telegram_buyer)

            data["search_result_buyer"] = search_result

        return await handler(event, data)


class BuyerSearchWhenReceivingDataFromWebApp(BaseMiddleware):
    async def __call__(
            self,
            handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]],
            event: Message,
            data: Dict[str, Any]
    ) -> Any:
        """
        Returns the buyer from the buyers table when
        receiving data from the webapp Telegram.

        :param handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]]
        :param event:  Message
        :param data: Dict[str, Any]
        :return: Buyers
        """

        if event.web_app_data:
            id_telegram_buyer = event.from_user.id

            search_result = \
                search_buyer_in_database(id_telegram=
                                         id_telegram_buyer)

            data["search_result_buyer"] = search_result

        return await handler(event, data)


class GetAllOrders(BaseMiddleware):
    async def __call__(
            self,
            handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]],
            event: Message,
            data: Dict[str, Any]
    ) -> Any:
        """
        Returns all the buyer's orders sorted from the last to
        the first number of orders. Responds to FSM State:
        EnteringNumberOrders().wait_number_orders.

        :param handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]]
        :param event: Message
        :param data: Dict[str, Any]
        :return: int, Orders
        """

        search_fsm_state: str = "wait_number_orders"

        fsm_state: str = data['raw_state']

        if fsm_state:
            fsm_state: list = fsm_state.split(":")
            fsm_state: str = fsm_state[1]

        if fsm_state == search_fsm_state:

            id_telegram_buyer = event.from_user.id

            orders = \
                search_all_orders_buyer_in_database(id_telegram=
                                                    id_telegram_buyer)

            prepared_list_orders: list = []

            for order in orders:

                list_dishes = \
                    json.loads(order.list_dishes)

                dishes = []

                for one_dish in list_dishes:
                    dish = search_dish_in_database(id_food=
                                                   list(one_dish.keys())[0])

                    dishes.append({
                            "name_food": dish.name_food,
                            "description_food": dish.description_food,
                            "img_food": dish.img_food,
                            "price": dish.price,
                            "count": list(one_dish.values())[0]
                    })

                prepared_list_orders.append({
                        "time_order_receipt": order.time_order_receipt,
                        "dishes": dishes,
                        "cost_food": order.cost_food,
                        "cost_delivery": order.cost_delivery,
                        "full_cost": order.full_cost,
                        "date_and_time_delivery": order.date_and_time_delivery,
                        "delivery_address": order.delivery_address,
                        "payment_status": order.payment_status,
                        "delivery_status": order.delivery_status
                })

            data["number_orders_buyer"] = len(orders)
            data["prepared_list_orders"] = prepared_list_orders

        return await handler(event, data)


class SelectActionNewAddres(BaseMiddleware):
    async def __call__(
            self,
            handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]],
            event: Message,
            data: Dict[str, Any]
    ) -> Any:
        """
        Register an FSM State NewDeliveryAddress.wait_new_delivery_address.
        turns the buyer's last order.

        :param handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]]
        :param event: Message
        :param data: Dict[str, Any]
        :return: Orders
        """
        search_fsm_state: str = "wait_new_delivery_address"

        fsm_state: str = data['raw_state']

        if fsm_state:
            fsm_state: list = fsm_state.split(":")
            fsm_state: str = fsm_state[1]

        if fsm_state == search_fsm_state:

            id_telegram_buyer = event.from_user.id

            search_result = \
                search_last_order_buyer_in_database(id_telegram=
                                                    id_telegram_buyer)

            data["last_order_buyer"] = search_result

        return await handler(event, data)


class LastOrderBuyerStartPayment(BaseMiddleware):
    async def __call__(
            self,
            handler: Callable[[CallbackQuery, Dict[str, Any]], Awaitable[Any]],
            event: CallbackQuery,
            data: Dict[str, Any]
    ) -> Any:
        """
        Returns the buyer's last order when choosing payment.

        :param handler: Callable[[CallbackQuery, Dict[str, Any]], Awaitable[Any]]
        :param event: CallbackQuery
        :param data: Dict[str, Any]
        :return: Orders
        """

        search_callback_one: str = \
            'pay_or_change_delivery_location:pay'

        if search_callback_one == event.data:

            id_telegram: int = event.from_user.id

            last_order_buyer = \
                search_last_order_buyer_in_database(id_telegram=
                                                    id_telegram)

            data['last_order_buyer'] = last_order_buyer

        return await handler(event, data)
