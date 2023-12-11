import sqlite3
import datetime
from datetime import timedelta
import time
import requests
import json

def task1():

    #create settings.txt file and load the location data into the file using API.

    city_name= input('Location of yesterday?(city name): ')
    api_key = '672ec8dd608c8b5111f451d38c741461'
    api_call = 'https://api.openweathermap.org/geo/1.0/direct?q=' + city_name + '&appid=' + api_key

    json_geo = requests.get(api_call).json()
    json_geo_filtered_cityname = str(json_geo[0]['name'])
    json_geo_filtered_lat = str(json_geo[0]['lat'])
    json_geo_filtered_lon = str(json_geo[0]['lon'])

    text = json_geo_filtered_cityname + ',' + json_geo_filtered_lat + ',' + json_geo_filtered_lon + ','

    # Write location information to the file:

    with open("settings.txt", "w") as file:
        file.write(text)

    # Create sqlite Table
    db = sqlite3.connect("DATA.sqlite")
    cursor = db.cursor()

    db.execute("""CREATE TABLE IF NOT EXISTS Data (
        Date TEXT,
        Went_to_bed REAL,
        Woke_up REAL,
        Sport TEXT,
        Cigarettes INTEGER,
        Alcohol TEXT,
        Sleeping_hours REAL,
        Weather REAL,
        DayAnswer TEXT)
        """)
    db.commit()

    #Create Day Class and ask questions to the user. Then insert the answers to the Data.sqlite along with weather:

    class Day:

        def __init__(self, date, went_to_bed_str, woke_up_str, sport, cigarettes, alcohol,
                     sleeping_hours_str, weather, day_answer):
            self.date = date
            self.went_to_bed_str = went_to_bed_str
            self.woke_up_str = woke_up_str
            self.sport = sport
            self.cigarettes = cigarettes
            self.alcohol = alcohol
            self.sleeping_hours_str = sleeping_hours_str
            self.weather = weather
            self.day_answer = day_answer

            script = 'INSERT INTO Data (Date, Went_to_bed, Woke_up, Sport, Cigarettes, Alcohol, ' \
                     'Sleeping_hours, Weather, DayAnswer)  VALUES (?,?,?,?,?,?,?,?,?);'
            new_day_info = (date, went_to_bed_str, woke_up_str, sport, cigarettes, alcohol,
                            sleeping_hours_str, weather, day_answer)

            db = sqlite3.connect("DATA.sqlite")
            cursor = db.cursor()
            cursor.execute(script, new_day_info)

            # Avoid duplicates (double input in one day)

            cs = db.execute("SELECT Date FROM Data")
            rows = cs.fetchall()
            last_entered_date = str(rows[-2])
            yesterday_check_txt = "('" + date + "',)"

            if len(rows) == 1:
                db.commit()
                print("You have successfully entered yesterday's data.!")
            elif yesterday_check_txt != last_entered_date:
                db.commit()
                print("You have successfully entered yesterday's data..!")
            else:
                print("ERROR: You have already filled yesterday's data!")


        @classmethod
        def new_day(cls):

            # Question date

            today = datetime.date.today()
            yesterday = today - datetime.timedelta(days=1)
            date = str(yesterday)

            # Question went_to_bad

            went_to_bed_hour = float(input('When did you go to bed?-(hh): '))
            went_to_bed_minute = float(input('When did you go to bed?-(mm): '))
            went_to_bed = timedelta(hours=went_to_bed_hour, minutes=went_to_bed_minute)
            #Below, I had to change the type to string to write the data on the sqlite3 database. Otherwise it gave me errors.
            went_to_bed_str = str(went_to_bed)

            # Question woke_up

            woke_up_hour = float(input('When did you wake up?-(hh): '))
            woke_up_minute = float(input('When did you wake up?-(mm): '))
            woke_up = timedelta(hours=woke_up_hour, minutes=woke_up_minute)
            #Below, I had to change the type to string to write the data on the sqlite3 database. Otherwise it gave me errors.
            woke_up_str = str(woke_up)

            # Question sport

            sport = input('Did you do sports?(Yes/No): ')

            # Question cigarettes

            cigarettes = int(input('How many cigarettes did you smoke?: '))

            # Question alcohol

            alcohol = input('Did you drink alcohol?(Yes/No): ')

            # Question sleeping_hours
            # 'd' variable is for getting a proper result. I found this solution for not getting a '-1 day' result when calculating sleeping hours.
            if went_to_bed_hour > 12:
                d = 1
            else:
                d = 0

            sleeping_hours = woke_up + timedelta(days=d) - went_to_bed
            #Below, I had to change the type to string to write the data on the sqlite3 database. Otherwise it gave me errors.
            sleeping_hours_str = str(sleeping_hours)

            # Question weather API

            # Read the file and get the location information:
            with open("settings.txt", "r") as file:
                lines = file.read()

            # Make list from string:
            l = list(lines.split(","))

            # Slice the list:
            lat_from_txt = l[-3]
            lon_from_txt = l[-2]

            #I converted predefined yesterday into UNIX format.
            yesterday_unix = str(int(time.mktime(yesterday.timetuple())))
            api_key = '672ec8dd608c8b5111f451d38c741461'
            url = 'https://api.openweathermap.org/data/2.5/onecall/timemachine?lat='+lat_from_txt+'&lon='\
                  +lon_from_txt+'&dt=' + yesterday_unix + '&appid=' + api_key
            json_data = requests.get(url).json()
            temp_k = json_data["current"]["temp"]

            #The result was in Kelvin, I converted it into Celsius.
            temp_c = round(temp_k - 273.15, 1)
            weather = temp_c

            # Question day_answer
            day_answer = input('How was yesterday?(Good/Normal/Bad): ')

            return cls(date, went_to_bed_str, woke_up_str, sport, cigarettes, alcohol, sleeping_hours_str, weather, day_answer)

    Day.new_day()

task1()