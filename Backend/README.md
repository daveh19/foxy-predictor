The API Documentation
==================

Guidelines on how to interact with the api and the kind of responses you should expect!

Install
-------

##### Requirements

- HTTPLib2 0.1+
- Python 3.0+


Design
-----

HTTP Verb | Example URI | Description | Parameters | Notes
------------ | ------------- | ------------- | ------------- | -------------
**GET** | *localhost:5000/parties/* | Allows fetching all the parties display name, abbreviation, leader, alliance. | - None | Check the sample code. <br> below.
**POST** | *localhost:5000/parties/* | Allows you to add a new party. | - name <br> - abbreviation <br> - leader <br> - alliance | Check the sample code. <br> below.



Usage
-----

##### All Parties Endpoint

Get a list of all parties

### Get Request from terminal!

``` python
    from getAllParties import getAllParties # from file_name import function_name
    getAllParties() # call function
```



