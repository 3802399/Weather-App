import requests
import json

class Weather:
    def __init__(self):
        self.api = 0
        self.get_api()
        self.code = 0
        self.msg = ""

        self.city = ""
        self.desc = ""
        self.country = ""

        self.temp = 0
        self.feels_like = 0
        self.temp_range = ()
        self.temp_method = ""

        self.humidity = 0
        self.wind_direction = ""
        self.wind_deg = 0
        self.wind_speed = 0
        self.visibility = 0

        self.icon = 0

        self.current_time = {
            "hour":0,
            "minute":0,
            "hour_type":0
        }

        self.sunrise = {
            "hour":0,
            "minute":0,
            "hour_type":0
        }

        self.sunset = {
            "hour":0,
            "minute":0,
            "hour_type":0
        }

    def get_api(self, city_name):
        url = f"http://api.openweathermap.org/data/2.5/weather?q={city_name}&appid={self.api}"
        response = requests.get(url)
        resp = response.json()

        self.code = resp["cod"]

        if self.code != 200:
            self.msg = resp["message"]
            return

        self.desc = resp["weather"]["description"]
        self.icon = resp["weather"]["icon"]

        self.temp = resp["main"]["temp"]
        self.feels_like = resp["main"]["feels_like"]
        self.temp_range = (resp["main"]["temp_min"], resp["main"]["temp_max"])
        self.temp_method = "K"

        self.humidity = resp["main"]["humidity"]
        self.visibility = resp["visibility"]

        self.wind_speed = resp["wind"]["speed"]
        self.wind_deg = resp["wind"]["deg"]

        self.country = resp["sys"]["country"]
        self.city = city_name

        self.sunrise
        self.sunset

        try:
            file = open("api_key", "r")
        except FileNotFoundError:
            return

        self.api = file.read()

        file.close()

    def get_weather(self):

            self.wind_direction = "W"
        elif self.wind_deg <= 340 or self.wind_deg > 290:
            self.wind_direction = "SW"

    def convert_to_dict(self):
        weather = {}

        weather["location"] = {
            "country":self.country,
            "city":self.city
        }

        weather["temp"] = {
            "temp":self.temp,
            "feels_like":self.feels_like,
            "min_max":self.temp_range
        }

        weather["humidity"] = self.humidity
        weather["visibility"] = self.visibility

        weather["desc"] = self.desc

        return weather

    def pretty_print(self):
        if self.code == 200:
            return  \
                f"""Weather for {self.city}, {self.country}

{self.desc}

TEMP
{self.temp} {self.temp_method}
Feels like: {self.feels_like} {self.temp_method}
Range: from {self.temp_range[0]} to {self.temp_range[1]} {self.temp_method}

Humidity: {self.humidity} %
Visibility: {self.visibility} km

Wind speed: {self.wind_speed} km/h {self.wind_direction}

Last updated (local time): {self.current_time['hour']}:{self.current_time['minute']} {['AM', 'PM'][self.current_time['hour_type']]}

Sunrise: {self.sunrise['hour']}:{self.sunrise['minute']} {['AM', 'PM'][self.sunrise['hour_type']]}
Sunset: {self.sunset['hour']}:{self.sunset['minute']} {['AM', 'PM'][self.sunset['hour_type']]}"""
        else:
            return f"Error: {self.msg}"
