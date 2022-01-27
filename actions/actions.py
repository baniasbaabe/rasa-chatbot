# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


import json
import requests
import datetime
import pandas as pd
from urllib.request import urlopen
from PIL import Image
from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import AllSlotsReset

def get_price(dish):
    
    df = pd.read_csv(r"dataframe/dishes.csv")

    filtered_df = df[df.Dish.str.contains(dish, case = False)]

    if filtered_df.empty:
        return None, None
    
    dish_name = filtered_df.iat[0, 0]
    dish_price = filtered_df.iat[0, 1]

    return dish_name, dish_price

class ActionGiveWeather(Action):

    def name(self) -> Text:
        return "action_give_weather"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        try:
            url = 'http://ipinfo.io/json'
            response = urlopen(url)
            data = json.load(response)

            city = data['city']

        except:
            dispatcher.utter_message(text = "Type in Google 'weather today' and you will find the answer ;)")
            return []

        try:
            url = "https://community-open-weather-map.p.rapidapi.com/weather"

            querystring = {"q":city,"units":"metric"}

            headers = {
                'x-rapidapi-host': "community-open-weather-map.p.rapidapi.com",
                'x-rapidapi-key': "425ee6975dmshef43068f62519e7p1c9496jsn0ff6d4e77085"
                }

            response = requests.request("GET", url, headers=headers, params=querystring)

            data = response.json()
        
        except:
            dispatcher.utter_message(text = f"Type in Google 'weather today {city}' and you will find the answer ;)")
            return []

        if data["weather"][0]["main"] == "Snow":
            weather = f"It is snowing!!! White white {city}."
        elif data["weather"][0]["main"] == "Rain":
            weather = "It is raining! Do not forget an umbrella."

        else:
            weather = f"We have {data['weather'][0]['main']}."

        if data["main"]["temp"] <= 3.0:
            temperature = f"The temperature is {data['main']['temp']} degrees Celsius and it feels like {data['main']['feels_like']} degrees Celsius. Minimum is {data['main']['temp_min']} and maximum is {data['main']['temp_max']} degrees Celsius. Brrrrr so cold."
        elif data["main"]["temp"] >= 25.0:
            temperature = f"The temperature is {data['main']['temp']} degrees Celsius and it feels like {data['main']['feels_like']} degrees Celsius. Kebab time?."
        else:
            temperature = f"The temperature is {data['main']['temp']} degrees Celsius and it feels like {data['main']['feels_like']} degrees Celsius."

        message = f"{weather} {temperature}"

        dispatcher.utter_message(text = message)

        return []

class ActionGiveDay(Action):

    def name(self) -> Text:
        return "action_give_day"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        weekday_dict = {
            0: "Monday",
            1: "Tuesday",
            2: "Wednesday",
            3: "Thursday",
            4: "Friday",
            5: "Saturday",
            6: "Sunday"
        }
        date = datetime.datetime.today()
        weekday = date.weekday()

        weekday = weekday_dict[weekday]

        message = f"Today is {weekday}, {date}."

        dispatcher.utter_message(text = message)

        return []

class ActionGiveFoodPrice(Action):

    def name(self) -> Text:
        return "action_give_food_price"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        dish_images = {
            "iskender": "assets/iskender.jpg",
            "cöpsis": "assets/coepsis.jpg",
            "dürüm": "assets/dueruem.jpg",
            "kaburga": "assets/kaburga.jpg",
            "lahmacun": "assets/lahmacun.jpg"
        }

        if len(tracker.latest_message["entities"]) == 0:
            message = "We don't offer your requested dish. Please take a look at our card: https://drive.google.com/file/d/1jnngcQxGkQL0m_B9C-RSf-GZkVdKJV1m/view?usp=sharing"

            dispatcher.utter_message(text = message)
            return []

        dish = tracker.latest_message["entities"][0]["value"].lower()

        dish_name, dish_price = get_price(dish)

        if dish_name and dish_price:
            message = f"{dish_name} costs {dish_price} € (Euro)."
        else:
            message = "We don't offer your requested dish. Please take a look at our card: https://drive.google.com/file/d/1jnngcQxGkQL0m_B9C-RSf-GZkVdKJV1m/view?usp=sharing"

        dispatcher.utter_message(text = message)

        try:
            img = Image.open(dish_images[dish])
            img.show()
        except:
            pass

        return []

class ActionConfirmReservation(Action):

    def name(self) -> Text:
        return "action_confirm_reservation"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        email = tracker.get_slot("email")
        time = tracker.get_slot("time")
        date = tracker.get_slot("date")

        message = f"We have noted your reservation.\nWhen? {date}\nTime? {time}\nEmail {email}"

        dispatcher.utter_message(text = message)

        return [AllSlotsReset()]