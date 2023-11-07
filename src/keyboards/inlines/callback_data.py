"""
Callback necessary for keyboard.
"""
from aiogram.filters.callback_data import CallbackData


class ChooseGenderWhenRegisteringBuyer(CallbackData,
                                       prefix="gender_buyer"):
    gender: str


class AnswerQuestionContinueRegistration(CallbackData,
                                         prefix="continue_registration"):
    answer_question_continue_registration: str


class AnswerQuestionLeaveReviewOrNot(CallbackData,
                                     prefix="leave_review_or_not"):
    answer_question_leave_review_or_not: str
    