"""
Class for FSM State
"""
from aiogram.fsm.state import StatesGroup, State


class ReviewsBuyer(StatesGroup):

    wait_negative_review = State()
    wait_positive_review = State()
