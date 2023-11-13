"""
Class in the module for FSM State used when
registering a user/buyer.
"""
from aiogram.fsm.state import StatesGroup, \
                              State


class BuyerRegistration(StatesGroup):
    """
    Used in buyer registration.
    """
    wait_name = State()
    wait_surname = State()
    wait_patronymic = State()
    wait_address = State()
    wait_birth_date = State()
    wait_gender = State()
    wait_question_register_or_not = State()
