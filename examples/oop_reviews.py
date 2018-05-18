import urllib.request, urllib.parse, urllib.error
import json
import sqlite3
from miner import get_places

from settings import CLIENT_ID, CLIENT_SECRET

# conn = sqlite3.connect('oop_reviews.sqlite')
# cur = conn.cursor()

# cur.execute('DROP TABLE IF EXISTS Counts')

# cur.execute('''CREATE TABLE Counts (review TEXT, count INTEGER)''')
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
                    # cur.execute('SELECT count FROM Counts WHERE review = ?', (tip['text'],))
                    # row = cur.fetchone()
                    # if row is None:
                        # cur.execute('''INSERT INTO Counts (review, count) VALUES (?, 1)''', (tip['text'],))
                    # else:
                        # cur.execute('UPDATE Counts SET count = count + 1 WHERE review = ?', (tip['text'],))
                    # conn.commit()
                # Reading all comments...

                if total - offset <= 0:
                    break
                else:
                    offset += limit
                # sqlstr = 'SELECT review, count FROM Counts ORDER BY count DESC LIMIT 10'
                # for row in cur.execute(sqlstr):
                    # print(str(row[0]), row[1])
        # Printing...
        for review in all_reviews:
            print(review)
        # cur.close()
        return all_reviews


a = Review("Bubble Waffle")
a.get_reviews()
