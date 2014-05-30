import requests
import json


class Pizza:
    @staticmethod
    def find(lat,lng,apikey):
        parameters = {'location': str(lat) + ',' + str(lng), 'sensor': 'false', 'key': apikey, 'rankby': 'distance', 'keyword': 'pizza'}
        data = requests.get('https://maps.googleapis.com/maps/api/place/nearbysearch/json',params=parameters)
        datadict = json.loads(data.content.decode("utf-8"))
        return datadict
