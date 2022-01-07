# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions



from typing import Any, Text, Dict, List

import json
import requests
import datetime
from urllib.request import urlopen


from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher

class ActionGiveLocation(Action):

    def name(self) -> Text:
        return "action_give_location"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        try:
            url = 'http://ipinfo.io/json'
            response = urlopen(url)
            data = json.load(response)

            IP = data['ip']
            org = data['org']
            city = data['city']
            country = data['country']
            region = data['region']

            message = f"I am living in {city}, {country}... Just like you ;)"
        except:
            message = "I am living in Stuttgart, DE."

        dispatcher.utter_message(text = message)

        return []

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
            weather = f"There is {data['weather'][0]['main']}"

        if data["main"]["temp"] <= 3.0:
            temperature = f"The temperature is {data['main']['temp']} and it feels like {data['main']['feels_like']}. Minimum is {data['main']['temp_min']} and maximum is {data['main']['temp_max']}. Brrrrr so cold."
        elif data["main"]["temp"] >= 25.0:
            temperature = f"The temperature is {data['main']['temp']}  and it feels like {data['main']['feels_like']}. BBQ time?."
        else:
            temperature = f"The temperature is {data['main']['temp']}  and it feels like {data['main']['feels_like']}."

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
