# Libraries
from flight_search import FlightSearch
from flight_alert import FlightAlert
from flight_database import FlightsDatabase
from datetime import datetime, timedelta
import pyshorteners

# Instances
fs = FlightSearch()
fa = FlightAlert()
fdb = FlightsDatabase()

# Variables
tomorrow = datetime.now() + timedelta(days=1)
two_years_from_today = datetime.now() + timedelta(days=(1 * 30))

# Set up Script
origin_city = str.title('fortaleza')
origin_code = fs.location_code(f'{origin_city}')
begin_date = tomorrow.date()
end_date = two_years_from_today.date()
cabin = 'C'
cabin_name = {'F': 'First Class', 'C': 'Business',
              'W': ' Premium Economy', 'M': 'Economy'}
adults = 2
kids = 0
baby = 0

# Setting up the Search Prices
ECONOMY_PRICE_COMPARE: int = 10000
BUSINESS_PRICE_COMPARE: int = 10000

# Getting Routes Values from the Database
routes = fdb.getting_data('destination')


# Return Messages Methods
def send_alert(attribute_economy_business, short_url, dest_code):
    """This Method is responsible for mount the Email Message"""

    message = f"\nPrice: {attribute_economy_business.price} R$"
    message += f"\nAdult Fare: {attribute_economy_business.adults_fare} R$"
    message += f"\nKid Fare: {attribute_economy_business.kids_fare} R$"
    message += f"\nBaby Fare: {attribute_economy_business.infants_fare} R$"
    message += f"\nSeats Left: {attribute_economy_business.seat}"
    message += f"\nAirline: {attribute_economy_business.airline}"
    message += f"\nTotal of Days: {attribute_economy_business.total_days}"
    message += f"\nBooking: {short_url}"
    message += f"\n"
    message += f"\nFlight Details"
    message += f"\n"
    message += f"\nDeparture :"
    message += f"\nOrigin: {attribute_economy_business.origin_city} - " \
               f"{attribute_economy_business.origin_airport}"
    message += f"\nDate: {attribute_economy_business.departure_date}"
    message += f"\nTime: {attribute_economy_business.departure_time}"
    message += f"\nFlight Number: {attribute_economy_business.departure_number}"
    message += f"\nAirplane: {attribute_economy_business.airplane_departure}"
    message += f"\n"
    message += f"\nReturn :"
    message += f"\nOrigin: {attribute_economy_business.destination_city} - " \
               f"{attribute_economy_business.destination_airport}"
    message += f"\nDate: {attribute_economy_business.return_date}"
    message += f"\nTime: {attribute_economy_business.return_time}"
    message += f"\nFlight Number: {attribute_economy_business.return_number}"
    message += f"\nAirplane: {attribute_economy_business.airplane_return}"

    fa.send_alert(subject=str.upper(
        f"Low price alert!!!! {origin_code} - {dest_code} "
        f"(Class : {cabin_name[attribute_economy_business.cabin_departure]})"), message=message)


def terminal_return(attribute_economy_business, origin, dest, price):
    print(f'{cabin_name[attribute_economy_business.cabin_departure]} Flight Found'
          f"\nLow price alert!!!! {origin} - {dest} "
          f"\nPrice: {price} R$")


# Main Loop
def flight_deals():
    """This Class is responsible for getting the cheapest flight every hour"""

    while isinstance(routes, type(None)) is False:

        for city in routes:
            dest_city = city['city']
            dest_code = city['iata']
            dest_id = city['id']

            print(f'Searching {dest_city}!!!\n')
            business = fs.flights(origin_code,
                                  city['iata'],
                                  begin_date,
                                  end_date,
                                  adults,
                                  kids,
                                  baby,
                                  cabin
                                  )

            economy = fs.flights(origin_code,
                                 city['iata'],
                                 begin_date,
                                 end_date,
                                 adults,
                                 kids,
                                 baby,
                                 None
                                 )

            # URL Shortener Object
            shortener = pyshorteners.Shortener()

            try:
                if business.price < BUSINESS_PRICE_COMPARE:

                    # URL
                    short_url = shortener.tinyurl.short(business.url)

                    # Terminal Return
                    terminal_return(business, origin_code, dest_code, business.price)

                    # Insert Flight Details
                    fdb.insert_details(business.departure_date, business.return_date,
                                       cabin_name[business.cabin_departure], business.seat, business.departure_number,
                                       business.return_number, business.total_days, business.price, short_url, dest_id)

                    fdb.update_season()

                    # Email Message
                    send_alert(business, short_url, dest_code)

                    print('Text/Email sent\n')

                elif economy.price < ECONOMY_PRICE_COMPARE:

                    # URL
                    short_url = shortener.tinyurl.short(economy.url)

                    # Terminal Return
                    terminal_return(economy, origin_code, dest_code, economy.price)

                    # Insert Flight Details
                    fdb.insert_details(economy.departure_date, economy.return_date,
                                       cabin_name[business.cabin_departure], economy.seat, economy.departure_number,
                                       economy.return_number, economy.total_days, economy.price, short_url, dest_id)

                    # Email Message
                    send_alert(economy, short_url, dest_code)
                    print('Text/Email sent\n')

                else:
                    print(f'No flight found to {dest_city}\n'
                          'Probably the flight is already full or does not exists at this point\n')
                    fdb.close()

            except Exception as error:
                print(str(error), '\n')


if __name__ == '__main__':
    flight_deals()
