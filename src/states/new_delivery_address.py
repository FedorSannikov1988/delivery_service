"""
Class in the module for FSM State used when
entering a new delivery address.
"""
from aiogram.fsm.state import StatesGroup, \
                              State


class NewDeliveryAddress(StatesGroup):
    """
    Throws it to the event handler in which a
    new delivery address is entered into the
    database.
    """
    wait_new_delivery_address = State()
