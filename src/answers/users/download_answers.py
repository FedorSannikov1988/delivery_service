"""
To download responses for users from files:
users_answers.json, button_names.json, urls.json
"""
from pathlib import Path
import json


def load_answer_for_user(path_for_file: str | Path):
    """
    Function for downloading data from files:
    button_names.json, urls.json, users_answers.json.
    The name of the files speaks for itself.

    :param path_for_file:
    :return: dict
    """

    try:
        with open(path_for_file, 'r', encoding='utf-8') as file_read_json:
            read_dict: dict = json.load(file_read_json)
            return read_dict

    except FileNotFoundError:
        empty_dict: dict = {}
        with open(path_for_file, 'w', encoding='utf-8') as file_create_json:
            json.dump(empty_dict, file_create_json)


#paths to data files
path_for_urls = \
    Path('answers', 'users', 'data_storage', 'urls.json')
path_for_users_answers = \
    Path('answers', 'users', 'data_storage', 'users_answers.json')
path_for_button_names = \
    Path('answers', 'users', 'data_storage', 'button_names.json')

