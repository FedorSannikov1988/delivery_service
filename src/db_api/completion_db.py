from .requests_db import add_one_dish_in_database, \
                         search_dish_in_database
from pathlib import Path
import json


def entering_data_into_table_food(path_for_file: str | Path):

    try:
        with open(path_for_file, 'r', encoding='utf-8') as file_read_json:
            all_food: dict = json.load(file_read_json)

        for dish in all_food:

            id_food = int(dish["id"][2:])

            search_result_id_food = \
                search_dish_in_database(id_food=id_food)

            if not search_result_id_food:

                add_one_dish_in_database(price=dish["price"],
                                         id_food=id_food,
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
