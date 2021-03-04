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

class ISS:
    def __init__(self):
        self.user_name = self.get_user_name()
        self.user_city = self.get_user_city()
        self.user_coordinates = self.get_user_coordinates()
        self.distance_in_km = self.calculate_distance()
        self.three_passtimes = get_iss_pass_time()


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
        message = f"""
        Welcome, {self.user_name}. Your distance from the ISS is {self.distance_in_km} km.
        The next three times the space station will pass {self.user_city}:
        
        
        """
        pass

    @staticmethod  # this method is static because 'self' is not used anywhere
    def get_user_name():
        return 'Sir Prise'

    def get_user_coordinates(self):
        """Lat and Long for Vienna, Austria"""
        return '48.210033', '16.363449'

    def get_user_city(self):
        """User city name"""
        return 'Vienna, Austria'

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
        return risetime_and_duration1, risetime_and_duration2, risetime_and_duration3

    def convert_unix_time(self, unix_timestamp):
        local_timezone = tzlocal.get_localzone()  # get pytz timezone

        local_time = datetime.fromtimestamp(unix_timestamp, local_timezone)
        print(local_time.strftime("%d.%m.%Y %H:%M:%S %z (%Z)"))

    def get_number_of_crew(self):
        """get info via: http://api.open-notify.org/astros.json"""
        pass

    def calculate_distance(self):
        return 1000


new = ISS()

print(new.get_iss_pass_time())

new.convert_unix_time(1614899040)
new.convert_unix_time(1614904746)
new.convert_unix_time(1614910555)
new.convert_unix_time(1614916384)
new.convert_unix_time(1614922197)






# %%

# %%

# %%

# %%

# %%

# %%

# %%
