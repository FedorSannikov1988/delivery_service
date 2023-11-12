"""
Class for FSM State
"""
from aiogram.fsm.state import StatesGroup, \
                              State


class EnteringNumberOrders(StatesGroup):

    wait_number_orders = State()
