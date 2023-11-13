"""
Callback for Inline Keyboard .
"""
from aiogram.filters.callback_data import CallbackData


class ChooseGenderWhenRegisteringBuyer(CallbackData,
                                       prefix=
                                       "gender_buyer"):
    """
    For Keyboard: get_gender_buyer_when_registering().
    """
    gender: str


class AnswerQuestionContinueRegistration(CallbackData,
                                         prefix=
                                         "continue_registration"):
    """
    For Keyboard: get_answer_question_continue_registration().
    """
    answer_question_continue_registration: str


class AnswerQuestionLeaveReviewOrNot(CallbackData,
                                     prefix=
                                     "leave_review_or_not"):
    """
    For Keyboard: leave_review_or_not().
    """
    answer_question_leave_review_or_not: str


class AnswerQuestionChoicePaymentOrChangeDeliveryLocation(CallbackData,
                                                          prefix=
                                                          "pay_or_change_delivery_location"):
    """
    For Keyboard: selection_for_registered_user().
    """
    payment_or_change_delivery_location: str
