import urllib.request, urllib.parse, urllib.error
import json
import csv

from settings import CLIENT_ID, CLIENT_SECRET

file = open('ukrainian.txt', encoding='utf-8', errors='ignore')
LOCATIONS = file.readlines()


def get_places(location):
    added = 0
    offset = 0
    limit = 50
    all_items = []
    url = "https://api.foursquare.com/v2/venues/explore"
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
            # print(res)

            items = res['groups'][0]['items']

            for item in range(len(items)):
                # print(res['groups'][0]['items'][item]['venue']['name'])
                added += 1
                all_items.append(
                    res['groups'][0]['items'][item]['venue']['name'])
            if limit - offset <= 0:
                break
            else:
                offset += limit

    return location, added, all_items


def write_in_file(items):
    with open('places.csv', "w", newline='', encoding="utf-8") as csv_file:
        writer = csv.writer(csv_file, delimiter=',', quotechar='"',
                            quoting=csv.QUOTE_ALL)
        for item in items:
            print(item)
            writer.writerow([item])


if __name__ == "__main__":
    data = get_places('Львів, Україна')
    items = data[2]
    write_in_file(items)
