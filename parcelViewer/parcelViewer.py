__author__ = 'lukeloreti'

import re, requests

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

    url = 'https://maps.googleapis.com/maps/api/streetview'
    appToken = 'AIzaSyD6Voni2-9GyirsyKyDT6Ng_l0_BxSLqjs'

    def collectPropertyStreetView(self, payload):

        payload['key'] = GoogleMapsApi.appToken
        resp = requests.get(GoogleMapsApi.url, params=payload)
        if resp.status_code != 200:
            # This means something went wrong.
            raise Exception('GET GoogleMapsApi {}'.format(resp.status_code))
        else:
            try:
                properties = resp.json()
            except ValueError:
                print "Did not receive a valid JSON object."

        return properties

c = CityDataApi()
g = GoogleMapsApi()

properties = c.request({'ptype' : '985'})
for p in properties:
    match = re.findall(r'-?\d+\.?\d*', p[location])
    x = float(match[0])
    y = float(match[1])

