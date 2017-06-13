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


Design
-----

HTTP Verb | Example URI | Description | Parameters | Notes
------------ | ------------- | ------------- | ------------- | -------------
**GET** | *localhost:5000/parties/* | Allows fetching all the parties display name, abbreviation, leader, alliance. | - None | Check the sample code. <br> below.
**GET** | *localhost:5000/parties/polls* | Allows you to fetch the polling data from all firms. | - None | Check the sample code. <br> below.



Usage
-----

### Parties Endpoint

Get a list of all parties

##### Get Request!

``` python
    from APICalls import getAllParties # from file_name import function_name
    getAllParties() # call function
```

### PollsEndpoint

Get a list of all parties

##### Get Request!

``` python
    from APICalls import getPollingData # from file_name import function_name
    getPollingData() # call function
```



