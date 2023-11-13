"""
Module with database queries.
Session loaded from connect_db.
"""
from .connect_db import SessionLocal
from sqlalchemy import desc, update
from .model_db import BookReviews, \
                      Buyers, \
                      Orders, \
                      Food
from datetime import datetime, \
                     date


session = SessionLocal()


def add_one_buyer_in_database(id_telegram: int,
                              telephone: str,
                              name: str,
                              surname: str,
                              patronymic: str,
                              birth_date: str,
                              gender: str,
                              default_adder_for_delivery: str,
                              confirmed_account: bool) -> None:
    """
    Adds the buyer after registration to the database.

    :param id_telegram: int
    :param telephone: str
    :param name: str
    :param surname: str
    :param patronymic: str
    :param birth_date: str
    :param gender: str
    :param default_adder_for_delivery:
    :param confirmed_account:
    :return: None
    """
    day, month, year = __to_create_date(input_date=birth_date)

    session.add(Buyers(id_telegram=id_telegram,
                       telephone=telephone,
                       name=name,
                       surname=surname,
                       patronymic=patronymic,
                       birth_date=date(day=day, month=month, year=year),
                       gender=gender,
                       default_adder_for_delivery=default_adder_for_delivery,
                       confirmed_account=confirmed_account))
    session.commit()
    session.close()


def search_buyer_in_database(id_telegram: int) -> Buyers:
    """
    Search for a buyer in the database by id.

    :param id_telegram: int
    :return: Buyers
    """
    resalt_request = session.query(Buyers).\
        filter(Buyers.id_telegram == id_telegram).first()
    session.close()
    return resalt_request


def add_one_review_buyer_in_database(id_telegram: int,
                                     dont_like: str,
                                     like: str) -> None:
    """
    Adding a review (record) to the table book_reviews.

    :param id_telegram: int
    :param dont_like: str
    :param like: str
    :return: None
    """
    session.add(BookReviews(id_telegram=id_telegram,
                            dont_like=dont_like,
                            like=like))
    session.commit()
    session.close()


def search_last_review_buyer_in_database(id_telegram: int) -> BookReviews:
    """
    Search for the buyer's last order.

    :param id_telegram:
    :return: BookReviews
    """
    resalt_request = session.query(BookReviews.date_and_time_creation).\
        filter(BookReviews.id_telegram == id_telegram).\
        order_by(desc(BookReviews.date_and_time_creation)).first()
    session.close()
    return resalt_request


def add_one_dish_in_database(price: float,
                             id_food: int,
                             img_food: str,
                             name_food: str,
                             description_food: str) -> None:
    """
    Adding new dishes to the food table.

    Used to add product data to the database
    after creating the database.

    :param price: float
    :param id_food: int
    :param img_food: str
    :param name_food: str
    :param description_food: str
    :return: None
    """
    session.add(Food(price=price,
                     id_food=id_food,
                     img_food=img_food,
                     name_food=name_food,
                     description_food=
                     description_food))
    session.commit()
    session.close()


def search_dish_in_database(id_food: int) -> Food:
    """
    Search for dishes by id in the database.

    :param id_food: int
    :return: None
    """
    resalt_request = session.query(Food).\
        filter(Food.id_food == id_food).first()
    session.close()
    return resalt_request


def add_one_order_in_database(id_telegram: int,
                              list_dishes: str,
                              cost_food: float,
                              cost_delivery: float,
                              full_cost: float,
                              delivery_date: str,
                              delivery_time: str,
                              delivery_address: str) -> None:
    """
    Adds an order to the database.

    :param id_telegram: int
    :param list_dishes: str
    :param cost_food: float
    :param cost_delivery: float
    :param full_cost: float
    :param delivery_date: str
    :param delivery_time: str
    :param delivery_address: str
    :return: None
    """
    day, month, year = __to_create_date(input_date=
                                      delivery_date)

    hours, minutes = __to_create_time(time=
                                    delivery_time)

    session.add(Orders(id_telegram=id_telegram,
                       list_dishes=list_dishes,
                       cost_food=cost_food,
                       cost_delivery=cost_delivery,
                       full_cost=full_cost,
                       date_and_time_delivery=
                       datetime(hour=hours, minute=minutes,
                                day=day, month=month, year=year),
                       delivery_address=delivery_address))
    session.commit()
    session.close()


def search_last_order_buyer_in_database(id_telegram: int) -> Orders:
    """
    Returns the last order made by the buyer.

    :param id_telegram:
    :return: Orders
    """
    resalt_request = session.query(Orders).\
        filter(Orders.id_telegram == id_telegram).\
        order_by(desc(Orders.id_order)).first()
    session.close()
    return resalt_request


def search_all_orders_buyer_in_database(id_telegram: int) -> list[Orders]:
    """
    Returns all the buyer's orders .
    The search for orders takes place by id_telegram.

    :param id_telegram: int
    :return: list[Orders]
    """
    resalt_request = session.query(Orders).\
        filter(Orders.id_telegram == id_telegram).\
        order_by(desc(Orders.id_order)).all()
    session.close()
    return resalt_request


def update_delivery_address_in_database(id_order: int,
                                        new_delivery_address: str) -> None:
    """
    Changes the delivery address table orders in the database.

    :param id_order: int
    :param new_delivery_address: str
    :return: None
    """
    update_query = update(Orders).where(Orders.id_order == id_order).values(
        delivery_address=new_delivery_address)
    session.execute(update_query)
    session.commit()
    session.close()


def update_payment_status_in_database(id_order: int,
                                      payment_status: bool) -> None:
    """
    Changes the payment status table orders in the database.

    :param id_order: int
    :param payment_status: bool
    :return: None
    """

    update_query = update(Orders).where(Orders.id_order == id_order).values(
        payment_status=payment_status)
    session.execute(update_query)
    session.commit()
    session.close()


def __to_create_date(input_date: str) -> tuple:
    """
    Parses the string variable to extract the
    day of the month and year from it .

    Used inside the module: requests_db .

    :param input_date: str
    :return: tuple
    """

    date_month_and_month_and_year: list[str] = input_date.split('.')

    day: int = int(date_month_and_month_and_year[0])
    month: int = int(date_month_and_month_and_year[1])
    year: int = int(date_month_and_month_and_year[2])

    return day, month, year


def __to_create_time(time: str) -> tuple:
    """
    Parses the string variable to extract
    hours and minutes from it.

    Used inside the module: requests_db .

    :param input_date: str
    :return: tuple
    """

    hours_minutes: list[str] = time.split(':')

    hours: int = int(hours_minutes[0])
    minutes: int = int(hours_minutes[1])

    return hours, minutes
