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


class ISS:
    def __init__(self):
        self.user_data = self.get_user_data()
        self.name = self.get_user_name()
        self.km = self.calculate_distance()

    @staticmethod
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
        Welcome, {self.name}. Your distance from the ISS is {km} km.
        The space station will pass {location} 
        
        """
        pass

    @staticmethod  # this method is static because 'self' is not used anywhere
    def get_user_name(self):
        return 'Sir Prise'

    def get_user_coordinates(self):
        pass

    def get_user_city(self):
        pass

    def get_iss_coordinates(self):
        """fetch position via: http://api.open-notify.org/iss-now.json"""
        json_data = self.make_requests("http://api.open-notify.org/iss-now.json")
        lat = json_data['iss_position']['latitude']
        long = json_data['iss_position']['longitude']
        return lat, long

    def get_iss_pass_time(self):
        """get info via: http://api.open-notify.org/iss-pass.json?lat=45.0&lon=-122.3"""
        pass

    def get_number_of_crew(self):
        """get info via: http://api.open-notify.org/astros.json"""
        pass

    def calculate_distance(self):
        return 1000


new = ISS()


print(new.get_iss_coordinates())



# %%

# %%

# %%

# %%

# %%

# %%

# %%
