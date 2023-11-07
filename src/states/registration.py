"""
Class for FSM State
"""
from aiogram.fsm.state import StatesGroup, State


class BuyerRegistration(StatesGroup):
    """
    Buyer registration chains.
    """
    wait_name = State()
    wait_surname = State()
    wait_patronymic = State()
    wait_address = State()
    wait_birth_date = State()
    wait_gender = State()
    wait_question_register_or_not = State()
