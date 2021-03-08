# ----------------------------------------------------------------------------
# Welcome to the real world, I hope you'll enjoy it!
# Author:           Steve-P42
# Description:      ISS - Information Request Interface
# Creation date:    2021-02-27 16:07:45
# Status:           in development
# ----------------------------------------------------------------------------
# %%
import urllib.request
import json
from datetime import datetime
import tzlocal  # pip install tzlocal
import haversine  # pip install haversine -> this is for distance calculations
from geopy.geocoders import Nominatim  # pip install geopy -> to get coordinates by location


# todo use asyncio to make the requests aat the same time
class ISS:
    def __init__(self, name='Sir Prise', city='New York'):
        self.user_name = name  # self.get_user_name()
        self.user_city = city  # self.get_user_city()
        self.user_coordinates = self.get_user_coordinates()
        self.iss_coordinates = self.get_iss_coordinates()
        self.distance_in_km = self.calculate_distance()
        self.three_passtimes = self.get_iss_pass_time()
        self.number_of_crew = self.get_number_of_crew()

    def make_requests(self, source):
        openurl = urllib.request.urlopen(source)
        if openurl.getcode() == 200:
            data = openurl.read()
            json_data = json.loads(data)
            return json_data
        else:
            print("Error receiving data:", openurl.getcode())

    def display_message(self):
        """define message template for requested data"""
        message = \
            f"""
        Welcome, {self.user_name}. Your distance from the ISS is {round(self.distance_in_km, 2)} km.
        Your location is: {self.user_city}
        
        The next times the station is visible are:
        Risetime: {self.three_passtimes[0][0]}  Duration: {self.three_passtimes[0][1]}
        Risetime: {self.three_passtimes[1][0]}  Duration: {self.three_passtimes[1][1]}
        Risetime: {self.three_passtimes[2][0]}  Duration: {self.three_passtimes[2][1]}
        
        Currently, there are {self.number_of_crew} astronauts on the ISS.
        """
        print(message)

    def get_user_coordinates(self):
        """Lat and Long by Location"""
        try:
            geolocator = Nominatim(user_agent="ISS_project")
            location = geolocator.geocode(self.user_city)

            self.user_city = location.address
            return location.latitude, location.longitude

        # print(location.address)
        # print((location.latitude, location.longitude))
        # print(location.raw)

        except BaseException as e:
            print('Error message:', e)
            print('Location not found, used Paris as location instead.')
            self.user_city = 'Paris'
            return 48.8534, 2.3488  # Paris

    # def get_user_city(self):
    #     """User city name"""
    #     location = input('What is your location?\n')
    #     return location

    def get_iss_coordinates(self):
        """fetch position via: http://api.open-notify.org/iss-now.json"""
        json_data = self.make_requests('http://api.open-notify.org/iss-now.json')
        lat = json_data['iss_position']['latitude']
        long = json_data['iss_position']['longitude']
        return lat, long

    def get_iss_pass_time(self):
        """get info via: http://api.open-notify.org/iss-pass.json?lat=48.210033&lon=16.363449"""
        template = "http://api.open-notify.org/iss-pass.json?lat={}&lon={}"
        passtime_request_url = template.format(self.user_coordinates[0], self.user_coordinates[1])

        json_data = self.make_requests(passtime_request_url)
        risetime_and_duration1 = json_data['response'][0]
        risetime_and_duration2 = json_data['response'][1]
        risetime_and_duration3 = json_data['response'][2]

        r1 = self.convert_unix_time(risetime_and_duration1['risetime'])
        r2 = self.convert_unix_time(risetime_and_duration2['risetime'])
        r3 = self.convert_unix_time(risetime_and_duration3['risetime'])
        d1 = f"{risetime_and_duration1['duration'] // 60}:{risetime_and_duration1['duration'] % 60} (m:s)"
        d2 = f"{risetime_and_duration2['duration'] // 60}:{risetime_and_duration2['duration'] % 60} (m:s)"
        d3 = f"{risetime_and_duration3['duration'] // 60}:{risetime_and_duration3['duration'] % 60} (m:s)"

        return (r1, d1), (r2, d2), (r3, d3)

    # todo okay, something is off with the times^^, fix that
    # compare to these:
    # https://astroviewer.net/iss/de/beobachtung.php
    # https://spotthestation.nasa.gov/sightings/view.cfm?country=Austria&region=None&city=Vienna

    def convert_unix_time(self, unix_timestamp):
        local_timezone = tzlocal.get_localzone()  # get pytz timezone

        local_time = datetime.fromtimestamp(unix_timestamp, local_timezone)
        # print(local_time.strftime("%d.%m.%Y %H:%M:%S %z (%Z)"))
        return (local_time.strftime("%d.%m.%Y %H:%M:%S %z (%Z)"))

    def get_number_of_crew(self):
        """get info via: http://api.open-notify.org/astros.json"""
        json_data = self.make_requests('http://api.open-notify.org/astros.json')
        return json_data['number']

    def calculate_distance(self):
        loc1 = (float(self.user_coordinates[0]), float(self.user_coordinates[1]))
        loc2 = (float(self.iss_coordinates[0]), float(self.iss_coordinates[1]))
        distance = haversine.haversine(loc1, loc2)
        return distance


# %% class is created with the username and user location as inputs
# both in string format:


new = ISS('Jason Bourne', 'London')
new.display_message()