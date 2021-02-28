# ----------------------------------------------------------------------------
# Welcome to the real world, I hope you'll enjoy it!
# Author:           Steve-P42
# Description:      ISS - Information Request Interface
# Creation date:    2021-02-27 16:07:45
# Status:           in development
# ----------------------------------------------------------------------------
# %%

class ISS:
    def __init__(self):
        self.user_data = self.get_user_data()

    def get_user_data(self):
        """"get user data and save for further processing
            use: https://randomuser.me/api/?inc=gender,name,location,nat
        """
        return 1
        pass


    def display_message(self):
        """define message template for requested data"""
        pass


    def get_user_name(self):
        pass


    def get_user_coordinates(self):
        pass


    def get_user_city(self):
        pass


    def get_iss_coordinates(self):
        """fetch position via: http://api.open-notify.org/iss-now.json"""
        pass


    def get_iss_pass_time(self):
        """get info via: http://api.open-notify.org/iss-pass.json?lat=45.0&lon=-122.3"""
        pass


    def get_number_of_crew(self):
        """get info via: http://api.open-notify.org/astros.json"""
        pass


    def calculate_distance(self):
        pass



# %%

# %%

# %%

# %%

# %%

# %%

# %%

# %%
