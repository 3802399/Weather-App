import json

class Settings:
    # these first few open_file methods are just to make sure the file exists and is valid
    @staticmethod
    def open_file():
        file = open("settings", "r")
        file.close()

    @staticmethod
    def open_file_check_json():
        try:
            file = open("settings", "r")
        except FileNotFoundError:
            return None

        data = json.loads(file.read())

        file.close()
        
    # to make the rest of the methods in this class easier to write
    @staticmethod
    def get_data():
        # get file and make sure file exists
        try:
            file = open("settings", "r")
        except FileNotFoundError:
            return None

        # get data from file
        data = json.loads(file.read())
        file.close()

        return data

    @staticmethod
    def save_data(data):
        # get file
        try:
            file = open("settings", "w")
        except FileNotFoundError:
            return None

        # save data with indent of 4 so it doesn't look terrible if we open the raw JSON file
        json.dump(data, file, indent=4)
        file.close()

    @staticmethod
    def save_data_param(param, param_input):
        data = Settings.get_data()

        if param in data:
            data[param] = param_input

        Settings.save_data(data)

    @staticmethod
    def toggle_mode(param, modes):
        data = Settings.get_data()

        # make sure the parameter exists and there are only two modes to toggle
        if param not in data or len(modes) != 2:
            return

        current = data[param]

        # we can't toggle if there is no current mode
        if current not in modes:
            return

        index = 0

        for mode in modes:
            if current == mode:
                break

            index += 1

        # use not of index to get other, unused mode
        other_mode = modes[not index]
        # save it
        Settings.save_data_param(param, other_mode)

    # temp unit
    @staticmethod
    def save_temp_unit(unit):
        if unit in ["C", "K", "F"]:
            Settings.save_data_param("temp_unit", unit)

    @staticmethod
    def get_temp_unit():
        return Settings.get_data()["temp_unit"]

    # fav city
    @staticmethod
    def get_fav_cities():
        return Settings.get_data()["fav_cities"]

    @staticmethod
    def add_fav_city(city):
        fav_cities = Settings.get_fav_cities()

        if city not in fav_cities:
            fav_cities.append(city)
            Settings.save_data_param("fav_cities", fav_cities)

    @staticmethod
    def remove_fav_city(city):
        fav_cities = Settings.get_fav_cities()

        if city in fav_cities:
            fav_cities.remove(city)
            Settings.save_data_param("fav_cities", fav_cities)

    # display mode - gui, cli
    @staticmethod
    def get_display_mode():
        return Settings.get_data()["display"]

    @staticmethod
    def save_display_mode(mode):
        if mode in ["gui", "cli"]:
            Settings.save_data_param("display", mode)

    @staticmethod
    def toggle_display_mode():
        modes = ["gui", "cli"]
        Settings.toggle_mode("display", modes)

    # display color
    @staticmethod
    def get_display_color():
        return Settings.get_data()["display-color"]

    @staticmethod
    def save_display_color(color):
        if color in ["dark", "light"]:
            Settings.save_data_param("display-color", color)

    @staticmethod
    def toggle_display_color():
        modes = ["dark", "light"]
        Settings.toggle_mode("display-color", modes)

    # choice of map (view it on the web using Google Maps or in the app itself using some map module)
    @staticmethod
    def get_map():
        return Settings.get_data()["map"]

    @staticmethod
    def save_map(map):
        if map in ["web", "app"]:
            Settings.save_data_param("map", map)

    @staticmethod
    def toggle_map():
        modes = ["web", "app"]
        Settings.toggle_mode("map", modes)

class SettingsCLI:
    def __init__(self):
        print("SETTINGS\n\n")

        self.change_fav_temp()
        self.add_fav_cities()
        self.remove_fav_cities()
        self.change_display()
        self.change_display_color()
        self.change_map()

        print("\n")

    def add_fav_cities(self):
        print("-----------------------------\n")
        print("To add favourite city, simply enter the city name. To exit or continue without adding any city, hit enter without input.\n")

        while True:
            city = input("Enter city name to add: ")

            if city != "":
                # the method will only add the city to favourites if not unfavourited already
                Settings.add_fav_city(city)
            else:
                break

        print()

    def remove_fav_cities(self):
        print("-----------------------------\n")
        print("To remove favourite cities, simply enter the city names. To exit or continue without adding any city, hit enter without input.\n")

        while True:
            city = input("Enter city name to remove: ")

            if city != "":
                # the method will do nothing if the city is not already favourited
                Settings.remove_fav_city(city)
            else:
                break

        print()

    def change_toggle(self, acceptable_inputs, input_str, param):
        print("-----------------------------\n")

        user_input = " "
        acceptable_inputs.append("")

        while user_input not in acceptable_inputs:
            user_input = input(input_str)

        if user_input != "":
            Settings.save_data_param(param, user_input)

        print()

    def change_display(self):
        self.change_toggle(["gui", "cli"], "Enter display input (gui, cli) or hit enter to continue: ", "display")

    def change_fav_temp(self):
        self.change_toggle(["C", "F", "K"], "Enter favourite temp unit (C, F, K) or hit enter to continue: ", "temp_unit")

    def change_display_color(self):
        self.change_toggle(["light", "dark"], "Enter display color (light, dark) or hit enter to continue: ", "display-color")

    def change_map(self):
        self.change_toggle(["web", "app"], "Enter how you want to view a map (web, app) or hit enter to continue: ", "map")

if __name__ == "__main__":
    SettingsCLI()
