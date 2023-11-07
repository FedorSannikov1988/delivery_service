from .model_db import Buyers, BookReviews
from .connect_db import SessionLocal
from sqlalchemy import desc
from datetime import date


session = SessionLocal()


def add_one_buyer_database(id_telegram: int,
                           telephone: str,
                           name: str,
                           surname: str,
                           patronymic: str,
                           birth_date: str,
                           gender: str,
                           default_adder_for_delivery: str,
                           confirmed_account: bool) -> None:

    date_month_and_month_and_year: list[str] = birth_date.split('.')
    date_month: int = int(date_month_and_month_and_year[0])
    month: int = int(date_month_and_month_and_year[1])
    year: int = int(date_month_and_month_and_year[2])

    session.add(Buyers(id_telegram=id_telegram,
                       telephone=telephone,
                       name=name,
                       surname=surname,
                       patronymic=patronymic,
                       birth_date=date(year, month, date_month),
                       gender=gender,
                       default_adder_for_delivery=default_adder_for_delivery,
                       confirmed_account=confirmed_account))
    session.commit()
    session.close()


def search_buyer(id_telegram: int):
    resalt_request = session.query(Buyers).\
        filter(Buyers.id_telegram == id_telegram).first()
    session.close()
    return resalt_request


def add_one_review_buyer_database(id_telegram: int,
                                  dont_like: str,
                                  like: str) -> None:

    session.add(BookReviews(id_telegram=id_telegram,
                            dont_like=dont_like,
                            like=like))
    session.commit()
    session.close()


def search_last_review_buyer_database(id_telegram: int):
    resalt_request = session.query(BookReviews.date_and_time_creation). \
        filter(BookReviews.id_telegram == id_telegram). \
        order_by(desc(BookReviews.date_and_time_creation)).first()
    session.close()
    return resalt_request
