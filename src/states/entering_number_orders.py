"""
Class in the module for FSM State used when
receiving all orders for a specific user.
"""
from aiogram.fsm.state import StatesGroup, \
                              State


class EnteringNumberOrders(StatesGroup):
    """
    Used to request the number of orders
    from the database for a specific user.
    """
    wait_number_orders = State()
