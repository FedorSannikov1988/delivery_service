"""
The module is responsible for registering the user in the database .
"""
from .processing_data_from_web_app import processing_order_after_registration
from keyboards import get_answer_question_continue_registration, \
                      AnswerQuestionContinueRegistration, \
                      get_gender_buyer_when_registering, \
                      ChooseGenderWhenRegisteringBuyer
from validation import ValidationRegistrations
from db_api import add_one_buyer_in_database
from aiogram.fsm.context import FSMContext
from aiogram.utils.markdown import hbold
from aiogram.types import CallbackQuery
from loader import router_for_main_menu
from states import BuyerRegistration
from datetime import timedelta, \
                     datetime
from aiogram import types, F
from loader import bot


DATE_FORMAT: str = "%d.%m.%Y"
LOWER_AGE_YEARS = 18
UPPER_AGE_YEARS = 100
NUMBER_DAYS_PER_YEAR: int = 365
MAX_LEN_NAME_SURNAME_PATRONYMIC: int = 35
QUESTIONS_DURING_REGISTRATION: dict = \
    {
        "id_telegram_buyer": "Id учетной записи telegram",
        "telephone_buyer": "Номер телефона",
        "name_buyer": "Имя",
        "surname_buyer": "Фамилия",
        "patronymic_buyer": "Отчество",
        "birth_date_buyer": "Дата рождения",
        "gender_buyer": "Пол",
        "default_adder_for_delivery_buyer": "Адрес доставки"
    }


@router_for_main_menu.message(F.contact)
async def start_registration(message: types.Message,
                             state: FSMContext,
                             search_result_buyer):
    """
    Start user registration (getting the user's contact).

    :param message: types.Message
    :param state: FSMContext
    :param search_result_buyer: Buyers
    :return: None
    """
    if message.contact.user_id == message.from_user.id:

        id_telegram_buyer = message.contact.user_id
        telephone_buyer = message.contact.phone_number

        if not search_result_buyer:

            await state.update_data({
                'id_telegram_buyer': id_telegram_buyer,
                'telephone_buyer': telephone_buyer
            })

            await state.set_state(BuyerRegistration.wait_name)

            text: str = f"Введите Ваше {hbold('имя')} "\
                        f"(с большой буквы без пробелов "\
                        f"только буквами русского алфавита):"
        else:

            text: str = "Вы уже зарегестрированы"

        await message.answer(text=text)


@router_for_main_menu.message(BuyerRegistration.wait_name)
async def entering_name_buyer(message: types.Message,
                              state: FSMContext):
    """
    Entering name buyer.

    :param message: types.Message
    :param state: state: FSMContext
    :return: None
    """
    name_buyer = message.text

    if ValidationRegistrations().validation_name_surname_patronymic(
            max_len=MAX_LEN_NAME_SURNAME_PATRONYMIC, text=name_buyer):

        await state.update_data({'name_buyer': name_buyer})
        await state.set_state(BuyerRegistration.wait_surname)

        text: str = f"Введите Вашу {hbold('фамилию')} "\
                    f"(с большой буквы без пробелов "\
                    f"только буквами русского алфавита):"

    else:

        text: str = f"Введите Ваше {hbold('имя')} "\
                    f"(с большой буквы без пробелов "\
                    f"только буквами русского алфавита):"

    await message.answer(text=text)


@router_for_main_menu.message(BuyerRegistration.wait_surname)
async def entering_surname_buyer(message: types.Message,
                                 state: FSMContext):
    """
    Entering surname buyer.

    :param message: types.Message
    :param state: FSMContext
    :return: None
    """
    surname_buyer = message.text

    if ValidationRegistrations().validation_name_surname_patronymic(
            max_len=MAX_LEN_NAME_SURNAME_PATRONYMIC, text=surname_buyer):

        await state.update_data({'surname_buyer': surname_buyer})
        await state.set_state(BuyerRegistration.wait_patronymic)

        text: str = f"Введите Ваше {hbold('отчество')} "\
                    f"(с большой буквы без пробелов "\
                    f"только буквами русского алфавита):"

    else:

        text: str = f"Введите Вашу {hbold('фамилию')} "\
                    f"(с большой буквы без пробелов "\
                    f"только буквами русского алфавита):"

    await message.answer(text=text)


@router_for_main_menu.message(BuyerRegistration.wait_patronymic)
async def entering_patronymic_buyer(message: types.Message,
                                    state: FSMContext):
    """
    Entering patronymic buyer.

    :param message: types.Message
    :param state: FSMContext
    :return: None
    """
    patronymic_buyer = message.text

    if ValidationRegistrations().validation_name_surname_patronymic(
            max_len=MAX_LEN_NAME_SURNAME_PATRONYMIC, text=patronymic_buyer):

        await state.update_data({'patronymic_buyer': patronymic_buyer})
        await state.set_state(BuyerRegistration.wait_gender)

        text: str = f"Введите Вашу {hbold('дату рождения')} " \
                    f"в формаме {hbold('дд.мм.гггг')} " \
                    f"{hbold('(пример 01.15.2023) ')} "

    else:

        text: str = f"Введите Ваше {hbold('отчество')} " \
                    f"(с большой буквы без пробелов " \
                    f"только буквами русского алфавита):"

    await message.answer(text=text)


@router_for_main_menu.message(BuyerRegistration.wait_gender)
async def entering_gender_buyer(message: types.Message,
                                state: FSMContext):
    """
    Entering gender buyer.

    :param message: types.Message
    :param state: FSMContext
    :return: None
    """
    birth_date_buyer = message.text

    if ValidationRegistrations().validation_data(
            date_string=message.text,
            format_date=DATE_FORMAT):

        await state.set_state()

        for_lower_bound: timedelta = \
            timedelta(days=
                      NUMBER_DAYS_PER_YEAR * LOWER_AGE_YEARS)
        for_upper_bound: timedelta = \
            timedelta(days=
                      NUMBER_DAYS_PER_YEAR * UPPER_AGE_YEARS)

        date_now: datetime = datetime.now()
        lower_bound = \
            date_now - for_lower_bound
        upper_bound = \
            date_now - for_upper_bound

        conversion_date = datetime.strptime(birth_date_buyer, DATE_FORMAT)

        if upper_bound <= conversion_date <= lower_bound:

            await state.update_data({'birth_date_buyer': birth_date_buyer})

            text: str = f"Введите Ваш {hbold('пол:')}"

            await message.answer(text=text,
                                 reply_markup=
                                 get_gender_buyer_when_registering())

        elif conversion_date >= lower_bound:

            text: str = "Регистрация доступна лицам достигшим " \
                        "18 лет включительно (процесс регистрации " \
                        "прерван)"
            await message.answer(text=text)
        else:

            text: str = "Регистрация не доступна лицам старше " \
                        "100 лет (процесс регистрации прерван)"
            await message.answer(text=text)

    else:

        text: str = f"Введите Вашу {hbold('дату рождения')} " \
                    f"в формаме {hbold('дд.мм.гггг')} " \
                    f"{hbold('(пример 01.15.2023) ')} "
        await message.answer(text=text)


@router_for_main_menu.callback_query(ChooseGenderWhenRegisteringBuyer.filter())
async def entering_default_adder_for_delivery(callback: CallbackQuery,
                                              callback_data: ChooseGenderWhenRegisteringBuyer,
                                              state: FSMContext):
    """
    Getting the selected gender of the buyer.

    :param callback: CallbackQuery
    :param callback_data: ChooseGenderWhenRegisteringBuyer
    :param state: FSMContext
    :return: None
    """
    chat_id = callback.message.chat.id
    gender_buyer = callback_data.gender

    await state.update_data({'gender_buyer': gender_buyer})
    await state.set_state(BuyerRegistration.wait_question_register_or_not)

    text: str = 'Введите Ваш адрес ' \
                '(по данному адресу будет ' \
                'осуществляться доставка):'
    args_for_send_message = {
        'text': text,
        'chat_id': chat_id
    }
    await bot.send_message(**args_for_send_message)


@router_for_main_menu.message(BuyerRegistration.wait_question_register_or_not)
async def data_verification_before_registration(message: types.Message,
                                                state: FSMContext):
    """
    Output of data previously entered by the user for verification.

    :param message: types.Message
    :param state: FSMContext
    :return: None
    """

    chat_id = message.chat.id
    default_adder_for_delivery = message.text

    await state.set_state()
    await state.update_data({
        'default_adder_for_delivery_buyer': default_adder_for_delivery
    })

    fsm_context: dict = await state.get_data()

    heading_text: str = "Пожалуйста проверьте " \
                        "введенные Вами ранее данные:"
    text_for_keyboard: str = "Зарегестрироваться:"

    args_for_send_message_heading = {
        'text': heading_text,
        'chat_id': chat_id
    }
    await bot.send_message(**args_for_send_message_heading)

    for key_for_fsm, question_text in QUESTIONS_DURING_REGISTRATION.items():
        text: str = question_text + ': ' + \
                    __handler_for_male_female(text=str(fsm_context[key_for_fsm]))

        args_for_send_message_text = {
            'text': text,
            'chat_id': chat_id
        }
        await bot.send_message(**args_for_send_message_text)

    args_for_send_message_keyboard = {
        'text': text_for_keyboard,
        'chat_id': chat_id,
        'reply_markup': get_answer_question_continue_registration()
    }
    await bot.send_message(**args_for_send_message_keyboard)


def __handler_for_male_female(text: str) -> str:
    """
    Processing the gender value coming from the database.
    Used inside the module.

    :param text: str
    :return: str
    """

    if text == 'F':
        return 'Женщина'

    if text == 'M':
        return 'Мужчина'

    return text


@router_for_main_menu.callback_query(AnswerQuestionContinueRegistration.filter())
async def confirmation_registration(callback: CallbackQuery,
                                    callback_data: AnswerQuestionContinueRegistration,
                                    state: FSMContext):
    """
    Processing the request (InlineKeyboar ->
    get_answer_question_continue_registration()) to register or not.

    :param callback: CallbackQuery
    :param callback_data: AnswerQuestionContinueRegistration
    :param state: FSMContext
    :return: None
    """
    chat_id: int = callback.message.chat.id
    message_id: int = callback.message.message_id
    answer: str = callback_data.answer_question_continue_registration

    await bot.delete_message(chat_id=chat_id,
                             message_id=message_id)

    fsm_context: dict = await state.get_data()

    if answer == "yes":

        text: str = "Вы зарегестрированы. " \
                    "Для активации аккаунта с Вами " \
                    "свяжутся в ближайшее время " \
                    "(в этой имитации работы аккаунт " \
                    "уже актевирован для дальнейшего " \
                    "тестирования)."

        keys_for_questions_during_registration = \
            list(QUESTIONS_DURING_REGISTRATION.keys())

        id_telegram_buyer: int = \
            fsm_context[keys_for_questions_during_registration[0]]
        telephone_buyer: str = \
            fsm_context[keys_for_questions_during_registration[1]]
        name_buyer: str = \
            fsm_context[keys_for_questions_during_registration[2]]
        surname_buyer: str = \
            fsm_context[keys_for_questions_during_registration[3]]
        patronymic_buyer: str = \
            fsm_context[keys_for_questions_during_registration[4]]
        birth_date_buyer: str = \
            fsm_context[keys_for_questions_during_registration[5]]
        gender_buyer: str = \
            fsm_context[keys_for_questions_during_registration[6]]
        default_adder_for_delivery_buyer: str = \
            fsm_context[keys_for_questions_during_registration[7]]

        # in working mode, it is assigned after a call from the manager
        confirmed_account: bool = True

        add_one_buyer_in_database(
            id_telegram=id_telegram_buyer,
            telephone=telephone_buyer,
            name=name_buyer,
            surname=surname_buyer,
            patronymic=patronymic_buyer,
            birth_date=birth_date_buyer,
            gender=gender_buyer,
            default_adder_for_delivery=
            default_adder_for_delivery_buyer,
            confirmed_account=confirmed_account)

    else:

        text: str = "Регистрация прервана"

    args_for_send_message = {
            'text': text,
            'chat_id': chat_id,
    }
    await bot.send_message(**args_for_send_message)

    if fsm_context.get('order'):
        await processing_order_after_registration(callback.message,
                                                  state)
