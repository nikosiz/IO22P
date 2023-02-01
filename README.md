# ToyStores

## Table of contents
* [Introduction](#Introduction)
* [Technologies](#Technologies)
* [Usage](#Usage)
* [Notice](#Notice)


## Introduction
This program is a part of ToyStores: Ceneo search project. Its main purpose is to scrap Ceneo page and provide IO22J part with ready product offers.  

## Technologies
* Python 3.2
* [Beautifulsoup 4.8.1](https://beautiful-soup-4.readthedocs.io/en/latest/) 
* [Flask 2.2](https://flask.palletsprojects.com/en/2.2.x/) 
* [Selenium](https://selenium-python.readthedocs.io/api.html)

## Usage

The request is sent using Request Param. First parameters the user provides are search phrases.
The last one specifies sorting.

| Parameter |   Sorting by:   |
|-----------|:---------------:|
| 0         |      price      |
| 1         | number of shops |


Assuming user request is:
```
www.example.com/search?product=lalka barbie&product=hot wheels&sorting=0
```
Function returns product offers using JSON. Ready result may look like this:

```json
[
  {
    "searchProduct": "lalka barbie",
    "resultProduct": {
      "id": "127060232",
      "name": "lalka barbie czarodziejka",
      "thumbnailUrl": "https://XYZ1",
      "offer": {
        "price": 21.37,
        "shippingPrice": 8.99,
        "seller": "XYZ",
        "redirectUrl": "https://XYZ2"
      }
    }
  },
  {
    "searchProduct": "hot wheels",
    "resultProduct": {
      "id": "312312",
      "name": "hot wheels big red car",
      "thumbnailUrl": "https://XYZ21",
      "offer": {
        "price": 22.21,
        "shippingPrice": 0.0,
        "seller": "X12YZ",
        "redirectUrl": "https://XYZ1322"
      }
    }
  }
]
```

## Notice
Program can return less product offers than the user is expecting.
It can mean, for example, that the product is unavailable, has only allegro offers or the search phrase provided was ambiguous.
It is recommended to try again with more precise request.
