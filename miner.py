import urllib.request, urllib.parse, urllib.error
import json
import time
import csv
from sqlalchemy import asc
import sys

from settings import CLIENT_ID, CLIENT_SECRET

file = open('ukrainian.txt', encoding='utf-8', errors='ignore')
LOCATIONS = file.readlines()


def get_places(location):
    added = 0
    offset = 0
    limit = 500
    url = "https://api.foursquare.com/v2/venues/search"
    sections = ['food', 'drinks', 'coffee', 'shops', 'arts', 'outdoors',
                'sights', 'trending', 'specials', 'topPicks', None]

    for section in sections:
        while True:
            params = {"client_id": CLIENT_ID, "client_secret": CLIENT_SECRET,
                      "near": location, "radius": "10000",
                      "limit": limit, "openNow": 0, "saved": 0, "specials": 0,
                      "offset": offset, "v": 20180301}
            if section is not None:
                params['section'] = section

            data = urllib.parse.urlencode(params)
            req = urllib.request.urlopen(url + "?" + data)
            res = json.loads(req.read().decode('utf-8'))['response']

            items = res['venues']
            total = len(res['venues'])

            for item in items:
                added += 1

            if total - offset <= 0:
                break
            else:
                offset += limit

    return location, added, items


def write_in_file(items):
    with open('places.csv', "w", newline='', encoding="utf-8") as csv_file:
        writer = csv.writer(csv_file, delimiter=',', quotechar='"',
                            quoting=csv.QUOTE_ALL)
        for item in items:
            # print(item['name'])
            writer.writerow([item['name']])


def get_reviews(place):
    offset = 0
    limit = 500
    added = 0
    interactions = {'liked': 1, 'meh': 0, 'disliked': -1}

    while True:
        url = "https://api.foursquare.com/v2/venues/%s/tips"
        data = urllib.parse.urlencode(
            {"client_id": CLIENT_ID, "client_secret": CLIENT_SECRET,
             "sort": "recent", "v": 20180301, 'limit': limit,
             'offset': offset})
        try:
            req = urllib.request.urlopen(url + "?" + data)
        except urllib.error.HTTPError:
            print('Waiting for 10 minutes...')
            time.sleep(600)
            continue

        res = json.loads(req.read().decode("utf-8"))['response']

        total = res['tips']['count']
        tips = res['tips']['items']

        for tip in tips:
            foursquare_id = tip['id']
            if 'authorInteractionType' not in tip:
                continue
            text = tip['text']

            added += 1

        if total - offset <= 0:
            break
        else:
            offset += limit

    return place.id, place.name, added


if __name__ == "__main__":
    data = get_places('Львів, Україна')
    items = data[2]
    write_in_file(items)