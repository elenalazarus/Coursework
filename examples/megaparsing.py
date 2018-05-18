from bs4 import BeautifulSoup

import requests


def megaparsing():
    url = "https://en.wikipedia.org/wiki/List_of_cities_in_Ukraine"

    r = requests.get(url)

    data = r.text

    soup = BeautifulSoup(data, "html5lib")

    letters = soup.find_all('td')
    letters = [letter.find('a') for letter in letters]
    stuff = []
    cities = []
    for letter in letters:
        try:
            a = letter['title']
            stuff.append(a)
        except TypeError:
            pass

    for s in stuff:
        if 'uk:' in s:
            if '(місто)' in s:
                cities.append(s[3:9])
            else:
                cities.append(s[3:])
            cities.append(stuff[stuff.index(s) - 1])

    cities = cities[:62]
    return cities