from .requests_db import add_one_dish
from pathlib import Path
import json


def entering_data_into_table_food(path_for_file: str | Path):

    try:
        with open(path_for_file, 'r', encoding='utf-8') as file_read_json:
            all_food: dict = json.load(file_read_json)

        for dish in all_food:
            add_one_dish(price=dish["price"],
                         id_food=int(dish["id"][2:]),
                         img_food=dish["img"],
                         name_food=dish["name"],
                         description_food=
                         dish["description"])

    except FileNotFoundError:
        empty_dict: dict = {}
        with open(path_for_file, 'w', encoding='utf-8') as file_create_json:
            json.dump(empty_dict, file_create_json)


path_for_fixtures = \
    Path('db_api', 'fixtures', 'food.json')
