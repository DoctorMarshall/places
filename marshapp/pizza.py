import requests
import json
from marshapp.rating import Rating

class Pizza:
    @staticmethod
    def find(user,lat,lng,apikey):
        parameters = {'location': str(lat) + ',' + str(lng), 'sensor': 'false', 'key': apikey, 'rankby': 'distance', 'keyword': 'pizza'}
        data = requests.get('https://maps.googleapis.com/maps/api/place/nearbysearch/json',params=parameters)
        datadict = json.loads(data.content.decode("utf-8"))
        datadict.update({'login' : user})
        for row in datadict['results']:
            row.update({'myrating' : Rating.getRating(user, row['id'])})
            row.update({'overalrating' : Rating.getAvgRating(row['id'])})
            row.update({'comments' : Rating.getComments(row['id'])})     
        return datadict
