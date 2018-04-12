import urllib.request, urllib.parse, urllib.error
import json
import time
from miner import get_places

from settings import CLIENT_ID, CLIENT_SECRET


class Review:
    """
    Search and print all reviews
    """

    def __init__(self, place):
        '''
        Initializing...
        :param place: str
        '''
        self.place = place
        self.web = []

    def foursquare_id(self):
        '''
        Looking for all ids of a place. Can be a franchise
        :return:
        '''
        web = []
        city = get_places("Львів")
        places = city[2]
        # All places
        for place in places:
            # Looking for user's place id
            if self.place in place and place[1] not in web:
                # Add id of every place
                web.append(place[1])
        return web

    def get_reviews(self):
        '''
        Get review from every place from franchise
        :return: lst
        '''
        all_reviews = []
        self.web = a.foursquare_id()
        for web in self.web:
            offset = 0
            limit = 500
            while True:
                # Make a request
                url = "https://api.foursquare.com/v2/venues/%s/tips" % web
                data = urllib.parse.urlencode(
                    {"client_id": CLIENT_ID, "client_secret": CLIENT_SECRET,
                     "sort": "recent", "v": 20180316, 'limit': limit,
                     'offset': offset})
                # Parsing...
                try:
                    req = urllib.request.urlopen(url + "?" + data)
                except urllib.error.HTTPError:
                    print('Waiting for 10 minutes...')
                    continue

                res = json.loads(req.read().decode("utf-8"))['response']

                total = res['tips']['count']
                tips = res['tips']['items']
                for tip in tips:
                    all_reviews.append(tip['text'])
                # Reading all comments...
                if total - offset <= 0:
                    break
                else:
                    offset += limit
        # Printing...
        for review in all_reviews:
            print(review)
        return all_reviews


a = Review("КебабШеф")
a.get_reviews()
