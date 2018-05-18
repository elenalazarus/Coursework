import os
import sys
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine

Base = declarative_base()


class Country(Base):
    __tablename__ = 'countries'
    id = Column(Integer, primary_key=True)
    country_name = Column(String(250), nullable=False)


class City(Base):
    __tablename__ = 'cities'
    id = Column(Integer, primary_key=True)
    country_id = Column(Integer, ForeignKey('countries.id'))
    city_name = Column(String(250), nullable=False)
    country = relationship(Country)


class Place(Base):
    __tablename__ = 'places'
    id = Column(Integer, primary_key=True)
    city_id = Column(Integer, ForeignKey('cities.id'))
    place_name = Column(String(250), nullable=False)
    city = relationship(City)


class Review(Base):
    __tablename__ = 'reviews'
    id = Column(Integer, primary_key=True)
    place_id = Column(Integer, ForeignKey('places.id'))
    review_text = Column(String(250), nullable=False)
    place = relationship(Place)


engine = create_engine('sqlite:///reviews.db')

Base.metadata.create_all(engine)