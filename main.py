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
import haversine  # pip install haversine -> this is for distance calculations
from geopy.geocoders import Nominatim  # pip install geopy -> to get coordinates by location


class ISS:
    def __init__(self, name='Sir Prise', city='New York'):
        self.user_name = name  # self.get_user_name()
        self.user_city = city  # self.get_user_city()
        self.user_coordinates = self.get_user_coordinates()
        self.iss_coordinates = self.get_iss_coordinates()
        self.distance_in_km = self.calculate_distance()
        self.three_passtimes = self.get_iss_pass_time()
        self.number_of_crew = self.get_number_of_crew()
        self.crew_names = self.get_crew_names()

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
        Risetime: {self.three_passtimes[3][0]}  Duration: {self.three_passtimes[3][1]}
        Risetime: {self.three_passtimes[4][0]}  Duration: {self.three_passtimes[4][1]}
        
        Currently, there are {self.number_of_crew} astronauts on the ISS.
        Their names are: {self.crew_names}.
        """
        print(message)

    def get_user_coordinates(self):
        """Lat and Long by Location"""
        try:
            geolocator = Nominatim(user_agent="ISS_project")
            location = geolocator.geocode(self.user_city)

            self.user_city = location.address
            print(location.latitude, location.longitude)
            return location.latitude, location.longitude

        except BaseException as e:
            print('Error message:', e)
            print('Location not found, used Paris as location instead.')
            self.user_city = 'Paris'
            return 48.8534, 2.3488  # Paris

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
        risetime_and_duration4 = json_data['response'][3]
        risetime_and_duration5 = json_data['response'][4]

        r1 = self.convert_unix_time(risetime_and_duration1['risetime'])
        r2 = self.convert_unix_time(risetime_and_duration2['risetime'])
        r3 = self.convert_unix_time(risetime_and_duration3['risetime'])
        r4 = self.convert_unix_time(risetime_and_duration4['risetime'])
        r5 = self.convert_unix_time(risetime_and_duration5['risetime'])
        d1 = f"{risetime_and_duration1['duration'] // 60}:{risetime_and_duration1['duration'] % 60} (m:s)"
        d2 = f"{risetime_and_duration2['duration'] // 60}:{risetime_and_duration2['duration'] % 60} (m:s)"
        d3 = f"{risetime_and_duration3['duration'] // 60}:{risetime_and_duration3['duration'] % 60} (m:s)"
        d4 = f"{risetime_and_duration4['duration'] // 60}:{risetime_and_duration4['duration'] % 60} (m:s)"
        d5 = f"{risetime_and_duration5['duration'] // 60}:{risetime_and_duration5['duration'] % 60} (m:s)"

        return (r1, d1), (r2, d2), (r3, d3), (r4, d4), (r5, d5)

    def convert_unix_time(self, unix_timestamp):

        return datetime.fromtimestamp(unix_timestamp).strftime("%d.%m.%Y %H:%M:%S")

    def get_number_of_crew(self):
        """get info via: http://api.open-notify.org/astros.json"""
        json_data = self.make_requests('http://api.open-notify.org/astros.json')
        return json_data['number']

    def get_crew_names(self):
        """get info via: http://api.open-notify.org/astros.json"""
        json_data = self.make_requests('http://api.open-notify.org/astros.json')
        crew_list = json_data['people']
        cr = []

        for i in crew_list:
            cr.append([i][0]["name"])
        names = ""
        for i in cr:
            names += i + ", "
        return names.rstrip().rstrip(',')

    def calculate_distance(self):
        loc1 = (float(self.user_coordinates[0]), float(self.user_coordinates[1]))
        loc2 = (float(self.iss_coordinates[0]), float(self.iss_coordinates[1]))
        distance = haversine.haversine(loc1, loc2)
        return distance


# %% class is created with the username and user location as inputs
# both in string format:


new = ISS('Jason Bourne', 'Vienna')
new.display_message()

#%%