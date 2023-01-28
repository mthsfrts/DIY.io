# Libraries
import psycopg2
import psycopg2.extras


class FlightsDatabase:
    """This class is responsible for connecting to the Database"""

    def __init__(self):

        self.conn = psycopg2.connect(

            host="Your DB server address",
            user="your-username",
            password="your-password",
            dbname="your-dbname",
            port=5432
        )
        self.cur = self.conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)

    def getting_data(self, table):
        try:
            self.cur.execute('select * from {}'.format(table))
            data = self.cur.fetchall()
            return data

        except Exception as error:
            print('Get Data Error: ' + str(error))
            return None

    def insert_city(self, iata, city):
        try:
            self.cur.execute("insert into destination(iata, city) values ({},{})".format(iata, city))
            self.conn.commit()

        except Exception as error:
            print('City Insert Error: ' + str(error))

    def update_iata(self, iata, city):
        try:
            self.cur.execute('UPDATE destination SET iata = {} WHERE city = {}'.format(iata, city))
            self.conn.commit()
            print(f"{city}'s IATA updated!")

        except Exception as error:
            print('IATA Update Error: ' + str(error))

    def insert_details(self, date1, date2, cabin, seats, flight1, flight2, total_days, price, url, dest_id):
        try:

            seats = seats if seats is not None else 'NULL'

            flights = "insert into details(departure_date, return_date, cabin, seats, departure_flight," \
                      "return_flight, total_days, price, url, destination_id) " \
                      "values('{}','{}','{}',{},{},{},{},{},'{}',{})".format(date1, date2, cabin, seats,
                                                                             flight1, flight2, total_days, price, url,
                                                                             dest_id)

            self.cur.execute(flights)
            self.conn.commit()
            print('Flight details saved into the database')

        except Exception as error:
            print('Flight Insert Error: ' + str(error))

    def update_season(self):
        try:
            season = self.cur.execute("Update details set season = CASE "
                                      "WHEN EXTRACT(MONTH from departure_date) < 3 THEN 'Winter' "
                                      "WHEN EXTRACT(MONTH from departure_date) = 3 THEN "

                                      "CASE WHEN EXTRACT(DAY from departure_date) <= 20 THEN 'Winter' ELSE "
                                      "'Transition to "
                                      "Spring' END "

                                      "WHEN EXTRACT(MONTH from departure_date) < 6 THEN 'Spring' "
                                      "WHEN EXTRACT(MONTH from departure_date) = 6 THEN "

                                      "CASE WHEN EXTRACT(DAY from departure_date) <= 20 THEN 'Spring' ELSE "
                                      "'Transition to "
                                      "Summer' END "

                                      "WHEN EXTRACT(MONTH from departure_date) < 9 THEN 'Summer' "
                                      "WHEN EXTRACT(MONTH from departure_date) = 9 THEN "

                                      "CASE WHEN EXTRACT(DAY from departure_date) <= 20 THEN 'Summer' ELSE "
                                      "'Transition to "
                                      "Autumn' END "

                                      "WHEN EXTRACT(MONTH from departure_date) < 12 THEN 'Autumn' "
                                      "WHEN EXTRACT(MONTH from departure_date) = 12 THEN "

                                      "CASE WHEN EXTRACT(DAY from departure_date) <= 20 THEN 'Autumn' ELSE "
                                      "'Transition to "
                                      "Winter' END "

                                      "END")
            self.conn.commit()
            return season

        except Exception as error:
            print('Season Update Error: ' + str(error))

    def close(self):
        try:
            self.cur.close()
            self.conn.close()

            print("Database connection is closed \n")

        except Exception as error:
            print(str(error))
