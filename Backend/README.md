The API Documentation
==================

Guidelines on how to interact with the api and the kind of responses you should expect!

Install
-------

##### Requirements for Python 3.0+:
Packages:
-json
-bs4
-pandas
-sqlalchemy
-flask

Modules
-----
APICalls.py:

Module handling the API endpoint calls to pull data from the database.
getAllParties: returns party names
getPollingData: returns a dictionary of polling data (one dataframe per firm)

models.py:

Module containing the table classes for the database.

endpoints.py:

Module creating the database engine and initializes a session.
Contains the the endpoints used to communicate with the database. 

extract_data.py:

Module for scraping the webpages containing our data sources
Pulls polling data from different sources and return them in a predefined format to push to the database.
Sources: Source object's class attribute 'sources'.


Design
-----

HTTP Verb | Example URI | Description | Parameters | Notes
------------ | ------------- | ------------- | ------------- | -------------
**GET** | *localhost:5000/parties/* | Allows fetching all the parties display name, abbreviation, leader, alliance. | - None | Check the sample code. <br> below.
**GET** | *localhost:5000/parties/polls* | Allows you to fetch the polling data from all firms. | - None | Check the sample code. <br> below.



Usage
-----

## Note 
You need to run endpoints.py to start the server. This runs a localhhost and hosts the REST API whih communicates with the database.

### Parties Endpoint

Get a list of all parties

##### Get Request!

``` python
    from APICalls import getAllParties # from file_name import function_name
    getAllParties() # call function
```

### PollsEndpoint

Get a list of polls from all firms

##### Get Request!

``` python
    from APICalls import getPollingData # from file_name import function_name
    getPollingData() # federal data 
    getPollingData(state=True) # state data
```



