from sqlalchemy import create_engine, func
from sqlalchemy.orm import sessionmaker
from miner import get_places

from bd_info import Country, City, Place, Review, Base

from megaparsing import megaparsing

cities = megaparsing()

engine = create_engine('sqlite:///reviews.db')

Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()


def add_country():
    new_country = session.query(Country).filter(
        Country.country_name == 'Ukraine').first()
    if new_country is None:
        new_country = Country(country_name='Ukraine')
    session.add(new_country)
    session.commit()
    print('Country added...')
    return new_country


def add_cities(new_country):
    all_cities = []
    for i, city in enumerate(cities):
        print(f"{i + 1}/{len(cities)} {city}")
        if len(session.query(City).filter(City.city_name == city).all()) == 0:
            new_city = City(city_name=city, country=new_country)
            session.add(new_city)
            all_cities.append(new_city)
    session.commit()
    print('Cities added...')
    return all_cities


def add_places(all_cities):
    for city in all_cities:
        print(city.city_name)
        data = get_places(city.city_name)
        places = data[2]
        print('Adding places in {}...'.format(city.city_name))
        for place in places:
            print(place)
            place2 = place[0]
            if len(session.query(Place).filter(
                            Place.place_name == place2).all()) == 0:
                new_place = Place(place_name=place2, city=city)
                session.add(new_place)
            try:
                session.commit()
            except:
                session.rollback()
            finally:
                session.close()
    session.commit()


def main():
    country = add_country()
    all_cities = add_cities(country)
    add_places(all_cities)


main()
