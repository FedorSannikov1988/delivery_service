"""
1 - Loading a token for a bot from environment variables
2 -
"""
from dotenv import load_dotenv
import os

load_dotenv()
TOKEN_BOT = os.getenv('TOKEN_FOR_BOT')
HOST_SERVER = os.getenv('HOST_SERVER')
PORT_SERVER = os.getenv('PORT_SERVER')
USER_LOG_IN_SERVER = os.getenv('USER_LOG_IN_SERVER')
PASSWORD_LOG_IN_SERVER = os.getenv('PASSWORD_LOG_IN_SERVER')
NAME_CREATED_DATABASE = os.getenv('NAME_CREATED_DATABASE')
NAME_MANAGER_CREATED_DATABASE = os.getenv('NAME_MANAGER_CREATED_DATABASE')
PASSWORD_MANAGER_CREATED_DATABASE = os.getenv('PASSWORD_MANAGER_CREATED_DATABASE')
