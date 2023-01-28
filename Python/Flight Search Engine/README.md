# Flight Deals Espresso

A flight search engine that looks up all the cheapest automatic taken as params the user needs.

The app will work with Gmail for send all the deals that will find, store all the data in a Google SQL INSTANCE for 
future reference, and will use the Kiwi API to query all the search and look-ups needed.

---

## **_Require Libraries :_**

* _Datetime (python native)_

* _Requests (python native)_

* _Psycopg2 and Psycopg2.extras (SQL - third part)_

* _SMTPLIB (python native)_

* _Email.message (python native)_

* _Pyshorteners (URL Shortener - third part)_

---

## **_Install Requirements :_**

To install all the requirements at once, for the engine to work, just run the **_code below_** 
in your terminal.

### _PS : Run the code inside the project folder_

### _**Bash Code :**_

**_pip3 install -r requirements.txt_**

---

## **_Database :_**

If you want to follow my idea you will need a database.

I used **_Google SQL INSTANCE : PostgreSQL_** as my main database, but feel free to choose whatever you want!

You will find everything that you need on this video : 

**_GCP Cloud SQL | Google Cloud Platform: For PostgreSQL | PgAdmin + SSL :_**

https://youtu.be/iBArrntzWcU

---

## **_Proxy Connection :_**

To run the database you will need a proxy connection. For get everything ready just follow the Google doc :

https://cloud.google.com/sql/docs/mysql/connect-admin-proxy

---
## **_Other :_**

If you have any comment or idea to increment on the engine fell free to reach out!

The **_'V.2'_** will probably take a machine learn or AI approach to make some advanced features, 
like price prediction for periods, cabin price prediction and a skipping-leg feature.


## **_Read All the Scripts to customize your credentials and settings_**