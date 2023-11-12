"""
Class for FSM State
"""
from aiogram.fsm.state import StatesGroup, \
                              State


class NewDeliveryAddress(StatesGroup):

    wait_new_delivery_address = State()
