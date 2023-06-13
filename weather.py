import requests
import json
import datetime
import settings

class Conversion:
    # the conversion functions used in this file
    @staticmethod
    def f_to_c(f):
        return (f - 32) * (5/9)

    @staticmethod
    def c_to_f(c):
        return c * (9/5) + 32

    @staticmethod
    def c_to_k(c):
        return c + 273.15

    @staticmethod
    def k_to_c(k):
        return k - 273.15

    @staticmethod
    def f_to_k(f):
        return (f - 32)/1.8 + 273.15

    @staticmethod
    def k_to_f(k):
        return (9/5) * (k - 273.15) + 32

    @staticmethod
    def ms_to_kmh(ms):
        s_in_m = 60
        m_in_hr = 60
        s_in_hr = s_in_m * m_in_hr

        mtrs_per_hour = ms * s_in_hr
        kmh = mtrs_per_hour/1000

        return kmh

    @staticmethod
    def convert_and_round(func, param, dec):
        return round(func(param), dec)

class Weather:
    def __init__(self, api):
        # variables for weather
        self.api = api
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
        self.pressure = 0

        self.icon = 0

        self.current_time = {
            "hour":0,
            "minute":0,
            "hour_type":0,
            "day":0,
            "month":0,
            "year":0
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

    def get_weather(self, city_name):
        # get weather data
        url = f"http://api.openweathermap.org/data/2.5/weather?q={city_name}&appid={self.api}"
        response = requests.get(url)
        resp = response.json()

        # check if weather data is valid
        self.code = resp["cod"]

        if self.code != 200:
            self.msg = resp["message"]
            return

        # get basic description and weather icon
        self.desc = resp["weather"][0]["description"]
        self.icon = resp["weather"][0]["icon"]

        # get temperature data
        self.temp = resp["main"]["temp"]
        self.feels_like = resp["main"]["feels_like"]
        self.temp_range = (resp["main"]["temp_min"], resp["main"]["temp_max"])
        self.temp_method = "K" # K is default for OpenWeatherMap

        fav_temp = settings.Settings.get_temp_unit()

        # if fav temp is valid and different, change it
        # if invalid, do not change
        if fav_temp in ["C", "F"]:
            funcs = {"C":Conversion.k_to_c, "F":Conversion.k_to_f}
            func = funcs[fav_temp]

            # so we don't manually type Conversion.convert_and_round over and over
            conv = Conversion.convert_and_round

            self.temp = conv(func, self.temp, 1)
            self.feels_like = conv(func, self.feels_like, 1)
            self.temp_range = (conv(func, self.temp_range[0], 1), conv(func, self.temp_range[1], 1))
            self.temp_method = fav_temp

        # humidity + visibility
        self.humidity = resp["main"]["humidity"]
        self.visibility = resp["visibility"]
        self.pressure = resp["main"]["pressure"]

        # get location
        self.coords = resp['coord']

        # wind speed stuff
        conv = Conversion.convert_and_round

        self.wind_speed = conv(Conversion.ms_to_kmh, resp["wind"]["speed"], 1)
        self.wind_deg = resp["wind"]["deg"]
        self.wind_direction = f"{self.wind_deg}"

        # get wind direction
        directions = {
            "W":[250, 290],
            "SW":[200, 250],
            "S":[160, 200],
            "SE":[110, 160],
            "E":[70, 110],
            "NE":[20, 70],
            "N":[340, 20],
            "NW":[290, 340]
        }

        # verify our data is valid
        if self.wind_deg >= 0 and self.wind_deg <= 360:
            # get direction frmo dict above
            for direction in directions:
                deg_limits = directions[direction]
                min = deg_limits[0]
                max = deg_limits[1]

                if max < min:
                    if self.wind_deg > min and self.wind_deg <= 360:
                        self.wind_direction = direction
                    elif self.wind_deg >= 0 and self.wind_deg <= max:
                        self.wind_direction = direction
                else:
                    if self.wind_deg > min and self.wind_deg <= max:
                        self.wind_direction = direction

        # country + city
        self.country = resp["sys"]["country"]
        self.city = city_name

        # sunrise
        tz = int(resp["timezone"])

        srise = int(resp['sys']['sunrise'])
        srise = datetime.datetime.utcfromtimestamp(srise + tz).strftime('%H:%M:%S')

        # the srise will be in format of H:M:S
        srise_hour = int(srise.split(":")[0])
        srise_min = srise.split(":")[1]
        srise_s = srise.split(":")[2]
        srise_hour_type = 0

        if srise_hour > 12:
            srise_hour -= 12
            srise_hour_type = 1
        elif srise_hour >= 12:
            # this is to show 12:XX PM if its the afternoon instead of 12:XX AM
            srise_hour_type = 1

        self.sunrise["hour"] = srise_hour
        self.sunrise["minute"] = srise_min
        self.sunrise["hour_type"] = srise_hour_type
        self.sunrise["second"] = srise_s

        # sunset
        sset = int(resp['sys']['sunset'])
        sset = datetime.datetime.utcfromtimestamp(sset + tz).strftime('%H:%M:%S')

        sset_hour = int(sset.split(":")[0])
        sset_min = sset.split(":")[1]
        sset_s = sset.split(":")[2]
        sset_hour_type = 0

        if sset_hour > 12:
            sset_hour -= 12
            sset_hour_type = 1
        elif sset_hour >= 12:
            # this is to show 12:XX PM if its the afternoon instead of 12:XX AM
            sset_hour_type = 1

        self.sunset["hour"] = sset_hour
        self.sunset["minute"] = sset_min
        self.sunset["hour_type"] = sset_hour_type
        self.sunset["second"] = sset_s

        # local time
        tz = datetime.timezone(datetime.timedelta(seconds=tz))
        entire_date = datetime.datetime.now(tz=tz).strftime("%m/%d/%Y %H:%M:%S")

        date = entire_date.split(" ")[0]
        time = entire_date.split(" ")[1]

        month = date.split("/")[0]
        day = date.split("/")[1]
        year = date.split("/")[2]

        hour = int(time.split(":")[0])
        minute = time.split(":")[1]
        second = time.split(":")[2]
        hour_type = 0

        if hour > 12:
            hour -= 12
            hour_type = 1
        elif hour >= 12:
            # this is to show 12:XX PM if its the afternoon instead of 12:XX AM
            hour_type = 1

        self.current_time["hour"] = hour
        self.current_time["minute"] = minute
        self.current_time["second"] = second
        self.current_time["hour_type"] = hour_type

        self.current_time["year"] = year
        self.current_time["month"] = month
        self.current_time["day"] = day

    def pretty_print(self):
        if self.code == 200:
            return  \
# get weather data in this format
            f"""{self.city.upper()}, {self.country}

{self.desc}

TEMP
{self.temp} {self.temp_method}
Feels like: {self.feels_like} {self.temp_method}
Range: from {self.temp_range[0]} to {self.temp_range[1]} {self.temp_method}

Humidity: {self.humidity} %
Visibility: {self.visibility} km
Pressure: {self.pressure} hPa

Wind speed: {self.wind_speed} km/h {self.wind_direction}

Last updated (local time): {self.current_time['hour']}:{self.current_time['minute']}:{self.current_time['second']} {['AM', 'PM'][self.current_time['hour_type']]}

Sunrise: {self.sunrise['hour']}:{self.sunrise['minute']}:{self.sunrise['second']} {['AM', 'PM'][self.sunrise['hour_type']]}
Sunset: {self.sunset['hour']}:{self.sunset['minute']}:{self.sunset['second']} {['AM', 'PM'][self.sunset['hour_type']]}"""
        else:
            return f"{self.city.upper()}, {self.country}\nError: {self.msg}"
