__author__ = 'lukeloreti'

from PIL import Image
from StringIO import StringIO
import multiprocessing, re, requests

class CityDataApi(object):

    url = 'https://data.cityofboston.gov/resource/n7za-nsjh.json'
    appToken = 'DuFPzI3bD5hphhji3gI3FJvPr'
    landUseCodes = {'A': 'Apartment Building',
          'C':'Commercial',
          'CD': 'Residential Condo Unit',
          'CM': 'Condo Main Building',
          'E': 'Exempt',
          'RC': 'Residential/Commercial',
          'RL': 'Residential Land',
          'R1': 'One Family',
          'R2': 'Two Family',
          'R3': 'Three Family',
          'R4': 'Four to Six Family'}

    def request(self, payload = None):

        properties = []
        resp = requests.get(CityDataApi.url, params=payload ,headers={'X-App-Token': CityDataApi.appToken})
        if resp.status_code != 200:
            # This means something went wrong.
            raise Exception('GET CityDataApi {}'.format(resp.status_code))
        else:
            try:
                properties = resp.json()
            except ValueError:
                print "Did not receive a valid JSON object."

        return properties

class GoogleMapsApi(object):

    streetUrl = 'https://maps.googleapis.com/maps/api/streetview'
    satelliteUrl = 'https://maps.googleapis.com/maps/api/staticmap'
    AppToken = 'AIzaSyD6Voni2-9GyirsyKyDT6Ng_l0_BxSLqjs'

    def collectPropertyView(self, x, y, type='satellite'):

        payload = {'key' : GoogleMapsApi.AppToken, 'size' : '600x400'}
        if type == 'street':
            url = GoogleMapsApi.streetUrl
            payload['location'] = x + ', ' + 'y'
        else:
            url = GoogleMapsApi.satelliteUrl
            payload['maptype'] = type
            payload['zoom'] = '19'
            payload['center'] = x + ', ' + y


        resp = requests.get(url, params=payload)
        if resp.status_code != 200:
            # This means something went wrong.
            raise Exception('GET GoogleMapsApi {}'.format(resp.status_code))
        else:
            try:
                i = Image.open(StringIO(resp.content))
                #i.show()
            except ValueError:
                print "Did not receive a valid JSON object."

        print "done"



c = CityDataApi()
g = GoogleMapsApi()

properties = c.request({'lu' : 'R1'})
for p in properties:
    match = re.findall(r'-?\d+\.?\d*', p['location'])
    x = match[0]
    y = match[1]
    g.collectPropertyView(x,y)

