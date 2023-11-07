from sqlalchemy.orm import relationship
from datetime import datetime
from .connect_db import Base
from sqlalchemy import ForeignKey, \
                       DateTime, \
                       Integer, \
                       Boolean, \
                       Column, \
                       String, \
                       Date


class Buyers(Base):
    __tablename__ = "buyers"

    id_telegram = Column(Integer, primary_key=True, autoincrement=False)
    telephone = Column(String(length=12), unique=True)
    name = Column(String(length=30))
    surname = Column(String(length=30))
    patronymic = Column(String(length=30))
    birth_date = Column(Date)
    gender = Column(String(length=1))
    default_adder_for_delivery = Column(String(length=250))
    confirmed_account = Column(Boolean)
    reviews = relationship("BookReviews", back_populates="buyer")


class BookReviews(Base):
    __tablename__ = "book_reviews"

    serial_number_record = Column(Integer, primary_key=True)
    id_telegram = Column(Integer, ForeignKey("buyers.id_telegram"))
    like = Column(String)
    dont_like = Column(String)
    date_and_time_creation = Column(DateTime, default=datetime.now)
    buyer = relationship("Buyers", back_populates="reviews")


class Food(Base):
    __tablename__ = "food"

    #id_food = Column(String, primary_key=True)
    id_food = Column(Integer, primary_key=True, autoincrement=False)
    name_food = Column(String)
    description_food = Column(String)
    img_food = Column(String)
    price = Column(Integer)
