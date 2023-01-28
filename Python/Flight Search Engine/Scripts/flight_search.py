# Libraries
import requests
from flight_details import FlightData

# Instances
server_v1 = 'https://tequila-api.kiwi.com'
server_v2 = 'https://tequila-api.kiwi.com/v2'

fd = FlightData

# Api key
with open('../keys/kiwi_key.txt', 'r') as cid:
    cid_txt = cid.read()


# Main Class
class FlightSearch:

    @staticmethod
    def location_code(city_name):
        location_endpoint = f'{server_v1}/locations/query'
        headers = {'apikey': f'{cid_txt}'}
        query = {'term': f'{city_name}', 'locations_types': 'city'}
        response = requests.get(url=location_endpoint,
                                headers=headers,
                                params=query)
        results = response.json()['locations']

        code = results[0]['code']
        return code

    @staticmethod
    def flights(origin_city, dest_city, begin_date, end_date, adults, kids, baby, cabin):
        check_endpoint = f'{server_v2}/search'
        headers = {'apikey': f'{cid_txt}'}
        class_search = 'Economy'
        query = {'fly_from': origin_city,
                 'fly_to': dest_city,
                 'date_from': begin_date.strftime("%d/%m/%Y"),
                 'date_to': end_date.strftime("%d/%m/%Y"),
                 'adults': adults,
                 'children': kids,
                 'infants': baby,
                 "nights_in_dst_from": 7,
                 "nights_in_dst_to": 28,
                 "flight_type": "round",
                 "one_for_city": 1,
                 "max_stopovers": 3,
                 "curr": "BRL",
                 "selected_cabins": ''
                 }

        if isinstance(cabin, type(None)) is False:
            class_search = 'Business'
            del query['one_for_city']
            query['selected_cabins'] = cabin

        response = requests.get(url=check_endpoint,
                                headers=headers,
                                params=query)
        try:
            results = fd.get_details(response)
            return results

        except IndexError as error:
            print(f"{class_search} Search Error!\n" +
                  str(error).title())
            return None
