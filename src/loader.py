"""
To download all the necessary data to
start the application /telegram bot
"""

from db_api import creating_database_for_app, Base, engine
from aiogram.fsm.storage.memory import MemoryStorage

from config import PASSWORD_MANAGER_CREATED_DATABASE, \
                   NAME_MANAGER_CREATED_DATABASE, \
                   NAME_CREATED_DATABASE, \
                   PASSWORD_LOG_IN_SERVER, \
                   USER_LOG_IN_SERVER, \
                   HOST_SERVER, \
                   PORT_SERVER
from aiogram import Dispatcher, Router, Bot, F
from answers import path_for_urls, \
                    load_answer_for_user, \
                    path_for_button_names, \
                    path_for_users_answers
from sqlalchemy.exc import OperationalError
from aiogram.enums import ParseMode
from config import TOKEN_BOT
from loguru import logger
import psycopg2


bot = Bot(token=TOKEN_BOT, parse_mode=ParseMode.HTML)

dp = Dispatcher(storage=MemoryStorage())

router_for_main_menu = Router()

router_for_main_menu.message.filter(F.chat.type == "private")

logger.add('logs/logs.json',
           level='DEBUG',
           format='{time} {level} {message}',
           rotation='10 MB',
           compression='zip',
           serialize=True)

# uploading responses for the user, button names, link urls (gif)
all_urls: dict = load_answer_for_user(path_for_file=
                                      path_for_urls)
button_names: dict = load_answer_for_user(path_for_file=
                                          path_for_button_names)
all_answer_for_user: dict = load_answer_for_user(path_for_file=
                                                 path_for_users_answers)

# creating database
try:
    creating_database_for_app(host_server=HOST_SERVER,
                              port_server=PORT_SERVER,
                              user_log_in_server=
                              USER_LOG_IN_SERVER,
                              password_log_in_server=
                              PASSWORD_LOG_IN_SERVER,
                              name_created_database=
                              NAME_CREATED_DATABASE,
                              name_manager_created_database=
                              NAME_MANAGER_CREATED_DATABASE,
                              password_manager_created_database=
                              PASSWORD_MANAGER_CREATED_DATABASE)
except psycopg2.OperationalError as create_database_error:
    logger.error(create_database_error)
except Exception as all_error_create_database:
    logger.error(all_error_create_database)

# creating all tables in database
try:
    Base.metadata.create_all(engine)
except OperationalError as create_table_error:
    logger.error(create_table_error)
except Exception as all_error_create_table:
    logger.error(all_error_create_table)
