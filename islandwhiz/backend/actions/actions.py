from typing import Any, Text, Dict, List
import mysql.connector
from mysql.connector import Error
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.types import DomainDict
from rasa_sdk.events import SlotSet

def connect_db():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="admin",
        database="travel_bot"
    )

def get_destination_id(cursor, destination: str):
    cursor.execute("SELECT DestinationID FROM destination WHERE Name = %s", (destination,))
    return cursor.fetchone()

class ActionListDestinations(Action):
    def name(self) -> Text:
        return "action_list_destinations"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: DomainDict) -> List[Dict[Text, Any]]:
        try:
            db = connect_db()
            cursor = db.cursor()
            cursor.execute("SELECT Name FROM destination")
            results = cursor.fetchall()
        except Error:
            dispatcher.utter_message(text="There was a problem accessing destination data.")
            return []
        finally:
            if db.is_connected():
                db.close()

        if results:
            destinations = ", ".join([r[0] for r in results])
            dispatcher.utter_message(text=f"Here are some popular destinations in Sri Lanka: {destinations}")
        else:
            dispatcher.utter_message(text="Sorry, I couldn't find any destinations at the moment.")
        return []

class ActionBestTimeToVisit(Action):
    def name(self) -> Text:
        return "action_best_time_to_visit"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: DomainDict) -> List[Dict[Text, Any]]:
        destination = tracker.get_slot("destination")
        if not destination:
            dispatcher.utter_message(text="Which destination are you interested in?")
            return []

        try:
            db = connect_db()
            cursor = db.cursor()
            dest = get_destination_id(cursor, destination)

            if dest:
                cursor.execute(""" 
                    SELECT BestSeason, RecommendedMonth, TemperatureRange 
                    FROM besttimetovisit 
                    WHERE DestinationID = %s
                """, (dest[0],))
                result = cursor.fetchone()
            else:
                dispatcher.utter_message(text=f"{destination} is not in my destination list.")
                return []
        except Error:
            dispatcher.utter_message(text="There was a problem retrieving the best time to visit.")
            return []
        finally:
            if db.is_connected():
                db.close()

        if result:
            season, month, temp_range = result
            dispatcher.utter_message(
                text=f"The best time to visit {destination} is during {season} (e.g., {month}). "
                     f"Typical temperatures are around {temp_range}.")
        else:
            dispatcher.utter_message(text=f"Sorry, I don't have best time info for {destination}.")
        return [SlotSet("destination", destination)]

class ActionTravelAdvice(Action):
    def name(self) -> Text:
        return "action_travel_advice"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: DomainDict) -> List[Dict[Text, Any]]:
        destination = tracker.get_slot("destination")
        if not destination:
            dispatcher.utter_message(text="Please tell me which destination you'd like advice about.")
            return []

        try:
            db = connect_db()
            cursor = db.cursor()
            dest = get_destination_id(cursor, destination)

            if dest:
                cursor.execute(""" 
                    SELECT AdviceDescription 
                    FROM traveladvice 
                    WHERE DestinationID = %s 
                    ORDER BY DateAdded DESC 
                    LIMIT 1
                """, (dest[0],))
                advice = cursor.fetchone()
            else:
                dispatcher.utter_message(text=f"{destination} is not recognized as a known destination.")
                return []
        except Error:
            dispatcher.utter_message(text="There was a problem retrieving travel advice.")
            return []
        finally:
            if db.is_connected():
                db.close()

        if advice:
            dispatcher.utter_message(text=f"Travel advice for {destination}: {advice[0]}")
        else:
            dispatcher.utter_message(text=f"No travel advice currently available for {destination}.")
        return [SlotSet("destination", destination)]

class ActionLiveInfo(Action):
    def name(self) -> Text:
        return "action_live_info"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: DomainDict) -> List[Dict[Text, Any]]:
        destination = tracker.get_slot("destination")
        if not destination:
            dispatcher.utter_message(text="Which destination would you like live updates for?")
            return []

        try:
            db = connect_db()
            cursor = db.cursor()
            dest = get_destination_id(cursor, destination)

            if dest:
                cursor.execute(""" 
                    SELECT Description, LiveStatus, UpdateTime 
                    FROM liveinfo 
                    WHERE DestinationID = %s 
                    ORDER BY UpdateTime DESC 
                    LIMIT 1
                """, (dest[0],))
                live_info = cursor.fetchone()
            else:
                dispatcher.utter_message(text=f"{destination} is not listed as a known destination.")
                return []
        except Error:
            dispatcher.utter_message(text="There was a problem retrieving live updates.")
            return []
        finally:
            if db.is_connected():
                db.close()

        if live_info:
            desc, status, update_time = live_info
            dispatcher.utter_message(
                text=f"Live update for {destination} ({status} as of {update_time}):\n{desc}")
        else:
            dispatcher.utter_message(text=f"No live updates available for {destination}.")
        return [SlotSet("destination", destination)]

class ActionDescribeDestination(Action):
    def name(self) -> Text:
        return "action_describe_destination"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: DomainDict) -> List[Dict[Text, Any]]:
        destination = tracker.get_slot("destination")
        if not destination:
            dispatcher.utter_message(text="Which destination would you like to know about?")
            return []

        try:
            db = connect_db()
            cursor = db.cursor()
            dest = get_destination_id(cursor, destination)

            if dest:
                cursor.execute(""" 
                    SELECT Description 
                    FROM destination 
                    WHERE DestinationID = %s
                    LIMIT 1
                """, (dest[0],))
                result = cursor.fetchone()
            else:
                dispatcher.utter_message(text=f"{destination} is not found in the destination database.")
                return []
        except Error:
            dispatcher.utter_message(text="There was a problem retrieving the destination description.")
            return []
        finally:
            if db.is_connected():
                db.close()

        if result:
            dispatcher.utter_message(text=f"Here's what I found about {destination}:\n{result[0]}")
        else:
            dispatcher.utter_message(text=f"Sorry, I couldn't find a description for {destination}.")
        return [SlotSet("destination", destination)]

class ActionSafetyTips(Action):
    def name(self) -> Text:
        return "action_safety_tips"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: DomainDict) -> List[Dict[Text, Any]]:
        destination = tracker.get_slot("destination")
        if not destination:
            dispatcher.utter_message(text="Please specify the destination you'd like safety tips for.")
            return []

        try:
            db = connect_db()
            cursor = db.cursor()
            dest = get_destination_id(cursor, destination)

            if dest:
                cursor.execute(""" 
                    SELECT AdviceDescription 
                    FROM traveladvice 
                    WHERE DestinationID = %s
                    ORDER BY DateAdded DESC 
                    LIMIT 1
                """, (dest[0],))
                tip = cursor.fetchone()
            else:
                dispatcher.utter_message(text=f"{destination} is not in the destination list.")
                return []
        except Error:
            dispatcher.utter_message(text="There was a problem retrieving safety tips.")
            return []
        finally:
            if db.is_connected():
                db.close()

        if tip:
            dispatcher.utter_message(text=f"Safety tips for {destination}: {tip[0]}")
        else:
            dispatcher.utter_message(text=f"No safety tips available for {destination}.")
        return [SlotSet("destination", destination)]

# Fallback action
class ActionDefaultFallback(Action):
    def name(self) -> Text:
        return "action_default_fallback"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: DomainDict) -> List[Dict[Text, Any]]:
        dispatcher.utter_message(text="Sorry, I didn't understand that. Could you rephrase?")
        return []
