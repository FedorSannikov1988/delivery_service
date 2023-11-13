"""
Loading all necessary parameters, addresses,
token, keys from environment variables.
"""
from dotenv import load_dotenv
import os

load_dotenv()

TOKEN_FOR_UPAY = os.getenv('TOKEN_FOR_UPAY')
TOKEN_BOT = os.getenv('TOKEN_FOR_BOT')
URL_FOR_WEB_APP = os.getenv('URL_FOR_WEB_APP')
HOST_SERVER = os.getenv('HOST_SERVER')
PORT_SERVER = os.getenv('PORT_SERVER')
USER_LOG_IN_SERVER = os.getenv('USER_LOG_IN_SERVER')
PASSWORD_LOG_IN_SERVER = os.getenv('PASSWORD_LOG_IN_SERVER')
NAME_CREATED_DATABASE = os.getenv('NAME_CREATED_DATABASE')
NAME_MANAGER_CREATED_DATABASE = os.getenv('NAME_MANAGER_CREATED_DATABASE')
PASSWORD_MANAGER_CREATED_DATABASE = os.getenv('PASSWORD_MANAGER_CREATED_DATABASE')
