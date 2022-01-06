# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


# This is a simple example for a custom action which utters "Hello World!"

from typing import Any, Text, Dict, List

import json
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
