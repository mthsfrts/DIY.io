# Classes
import json

import json


class FlightData:

    def __init__(self, price, adults_fare, kids_fare, infants_fare, airline,
                 airplane_departure, airplane_return, origin_city,
                 origin_airport, destination_city, destination_airport, departure_date,
                 return_date, departure_number, return_number, url, seat, cabin_departure, cabin_return,
                 total_days, departure_time, return_time):

        self.price = price
        self.adults_fare = adults_fare
        self.kids_fare = kids_fare
        self.infants_fare = infants_fare
        self.seat = seat
        self.airline = airline
        self.airplane_departure = airplane_departure
        self.airplane_return = airplane_return
        self.origin_city = origin_city
        self.origin_airport = origin_airport
        self.destination_city = destination_city
        self.destination_airport = destination_airport
        self.departure_date = departure_date
        self.return_date = return_date
        self.departure_number = departure_number
        self.return_number = return_number
        self.url = url
        self.cabin_departure = cabin_departure
        self.cabin_return = cabin_return
        self.total_days = total_days
        self.departure_time = departure_time
        self.return_time = return_time

    @staticmethod
    def get_details(response):
        """This Function is responsible for get and sort all the important details"""
        data = response.json()["data"][0]

        if len(data) > 0:
            return FlightData(
                price=data["price"],
                adults_fare=data["fare"]['adults'],
                kids_fare=data["fare"]['children'],
                infants_fare=data["fare"]["infants"],

                origin_city=data["route"][0]["cityFrom"],
                origin_airport=data["route"][0]["flyFrom"],

                destination_city=data["route"][1]["cityTo"],
                destination_airport=data["route"][1]["flyTo"],

                departure_date=data["route"][0]["local_departure"].split("T")[0],
                departure_time=data["route"][0]["local_departure"].split("T")[1].split("Z")[0],

                return_date=data["route"][2]["local_departure"].split("T")[0],
                return_time=data["route"][2]["local_departure"].split("T")[1].split("Z")[0],

                departure_number=data["route"][0]["flight_no"],
                return_number=data["route"][2]["flight_no"],

                seat=data["availability"]['seats'],
                url=data["deep_link"],

                cabin_departure=data["route"][0]["fare_category"],
                cabin_return=data["route"][2]["fare_category"],

                airline=data["airlines"][0],
                total_days=data["nightsInDest"],

                airplane_departure=data["route"][0]["equipment"],
                airplane_return=data["route"][2]["equipment"],
            )

        return None
