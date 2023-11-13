"""
The module is responsible for filling out the book of reviews about the service nomad.
"""
from keyboards import AnswerQuestionLeaveReviewOrNot
from db_api import add_one_review_buyer_in_database
from aiogram.fsm.context import FSMContext
from keyboards import leave_review_or_not
from aiogram.utils.markdown import hbold
from validation import ValidationReviews
from datetime import datetime, timedelta
from loader import router_for_main_menu
from aiogram.types import CallbackQuery
from aiogram.filters import Command
from states import ReviewsBuyer
from aiogram import types, F
from loader import bot


INTERVAL_IN_MINUTES_BETWEEN_REVIEWS: int = 60
MINIMUM_REVIEW_LENGHT_IN_CHARACTERS: int = 3
QUESTIONS_DURING_REVIEW: dict = \
    {
        "negative_review_buyer": "Не понравилось:",
        "positive_review_buyer": "Понравилось:"
    }


@router_for_main_menu.message(Command("reviews"))
@router_for_main_menu.message(F.text == "Книга отзывов")
async def start_reviews(message: types.Message,
                        state: FSMContext,
                        result_search_buyer,
                        last_review_buyer_from_db):
    """
    Reaction to a command /reviews or button press "Книга отзывов".

    :param message: types.Message
    :param state: FSMContext
    :param result_search_buyer: Buyers
    :param last_review_buyer_from_db: BookReviews
    :return: None
    """
    if result_search_buyer:

        if last_review_buyer_from_db:

            last_review_buyer_str = \
                str(last_review_buyer_from_db.date_and_time_creation)

            last_review_buyer =\
                datetime.strptime(last_review_buyer_str,
                                  '%Y-%m-%d %H:%M:%S.%f')

            time_next_review_possible = \
                last_review_buyer + timedelta(minutes=
                                              INTERVAL_IN_MINUTES_BETWEEN_REVIEWS)

            if time_next_review_possible <= datetime.now():

                await __start_reviews_good_answer(message=message,
                                                  state=state)

            else:

                text: str = \
                    f'Оставить следующий отзыв можно через ' \
                    f'{INTERVAL_IN_MINUTES_BETWEEN_REVIEWS} минут'
                await message.answer(text=text)
        else:

            await __start_reviews_good_answer(message=message,
                                              state=state)
    else:

        text: str = f'Оставлять отзывы могут только ' \
                    f'зарегестрированные пользователи'
        await message.answer(text=text)


async def __start_reviews_good_answer(message, state):
    text: str = f'Опишите что Вам {hbold("не понравилось:")}'
    await message.answer(text=text)
    await state.set_state(ReviewsBuyer.wait_negative_review)


@router_for_main_menu.message(ReviewsBuyer.wait_negative_review)
async def enter_negative_review(message: types.Message,
                                state: FSMContext):
    """
    Handler for receiving and processing (validating) negative feedback.

    :param message: types.Message
    :param state: FSMContext
    :return: None
    """
    negative_review = message.text

    if ValidationReviews().validation_long_reviews(
            text=negative_review,
            min_len=MINIMUM_REVIEW_LENGHT_IN_CHARACTERS):

        await state.update_data({'negative_review_buyer': negative_review})
        text: str = f'Опишите что Вам {hbold("понравилось:")}'
        await message.answer(text=text)
        await state.set_state(ReviewsBuyer.wait_positive_review)

    else:
        text: str = f'Опишите что Вам {hbold("не понравилось:")}'
        await message.answer(text=text)


@router_for_main_menu.message(ReviewsBuyer.wait_positive_review)
async def enter_positive_review(message: types.Message,
                                state: FSMContext):
    """
    Handler for receiving and processing (validating) positive feedback.

    :param message: types.Message
    :param state: FSMContext
    :return: None
    """
    positive_review = message.text

    if ValidationReviews().validation_long_reviews(
            text=positive_review,
            min_len=MINIMUM_REVIEW_LENGHT_IN_CHARACTERS):

        await state.update_data({'positive_review_buyer': positive_review})

        fsm_context: dict = await state.get_data()

        for key_for_fsm_context, name_questions in QUESTIONS_DURING_REVIEW.items():
            text: str = name_questions + ' ' + str(fsm_context[key_for_fsm_context])
            await message.answer(text=text)

        text: str = f'Оставить Ваш отзыв:'
        await message.answer(text=text,
                             reply_markup=
                             leave_review_or_not())
        await state.set_state()

    else:
        text: str = f'Опишите что Вам {hbold("понравилось:")}'
        await message.answer(text=text)


@router_for_main_menu.callback_query(AnswerQuestionLeaveReviewOrNot.filter())
async def confirmation_leaving_review(callback: CallbackQuery,
                                      state: FSMContext,
                                      callback_data: AnswerQuestionLeaveReviewOrNot):
    """
    Handler for output of previously entered
    reviews and confirmation of leaving a review.

    :param callback: CallbackQuery
    :param state: FSMContext
    :param callback_data: AnswerQuestionLeaveReviewOrNot
    :return: None
    """

    buyer_id: int = callback.from_user.id
    chat_id: int = callback.message.chat.id
    message_id: int = callback.message.message_id
    answer: str = callback_data.answer_question_leave_review_or_not

    await bot.delete_message(chat_id=chat_id,
                             message_id=message_id)

    if answer == 'yes':
        text: str = 'Спасибо Ваш отзыв отправлен'

        fsm_context: dict = await state.get_data()

        keys_for_negative_and_positive_review_buyer = \
            list(QUESTIONS_DURING_REVIEW.keys())

        negative_review_buyer: str = \
            fsm_context[keys_for_negative_and_positive_review_buyer[0]]

        positive_review_buyer: str = \
            fsm_context[keys_for_negative_and_positive_review_buyer[1]]

        add_one_review_buyer_in_database(
            id_telegram=buyer_id,
            dont_like=negative_review_buyer,
            like=positive_review_buyer)

    else:
        text: str = 'Ваш отзыв не отправлен'

    args_for_send_message = {
        'text': text,
        'chat_id': chat_id
    }
    await bot.send_message(**args_for_send_message)
