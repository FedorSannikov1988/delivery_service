"""
Class in the module for FSM State for customer reviews.
"""
from aiogram.fsm.state import StatesGroup, \
                              State


class ReviewsBuyer(StatesGroup):
    """
    Two states for entering customer reviews.
    """
    wait_negative_review = State()
    wait_positive_review = State()
