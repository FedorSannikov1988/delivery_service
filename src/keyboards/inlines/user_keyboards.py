"""
All keyboards for users .
"""
from aiogram.utils.keyboard import InlineKeyboardBuilder
from .callback_data import ChooseGenderWhenRegisteringBuyer, \
                           AnswerQuestionContinueRegistration, \
                           AnswerQuestionLeaveReviewOrNot


def get_gender_buyer_when_registering():
    """
    Keyboard for selecting gender buyer.

    :return: InlineKeyboardMarkup
    """
    builder = InlineKeyboardBuilder()

    builder.button(
        text='Мужчина',
        callback_data=ChooseGenderWhenRegisteringBuyer(
            gender='M')
        )

    builder.button(
        text='Женщина',
        callback_data=ChooseGenderWhenRegisteringBuyer(
            gender='F')
        )

    builder.adjust(2)

    return builder.as_markup()


def get_answer_question_continue_registration():
    builder = InlineKeyboardBuilder()

    builder.button(
        text='Да',
        callback_data=
        AnswerQuestionContinueRegistration(
            answer_question_continue_registration='yes')
        )

    builder.button(
        text='Нет',
        callback_data=
        AnswerQuestionContinueRegistration(
            answer_question_continue_registration='no')
        )

    builder.adjust(2)

    return builder.as_markup()


def leave_review_or_not():

    builder = InlineKeyboardBuilder()

    builder.button(
        text='Да',
        callback_data=
        AnswerQuestionLeaveReviewOrNot(
            answer_question_leave_review_or_not='yes')
        )

    builder.button(
        text='Нет',
        callback_data=
        AnswerQuestionLeaveReviewOrNot(
            answer_question_leave_review_or_not='no')
        )

    builder.adjust(2)

    return builder.as_markup()
