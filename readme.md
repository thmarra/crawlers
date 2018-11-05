# Crawlers
[![Python 3.5](https://img.shields.io/badge/python-3.5-blue.svg)](https://www.python.org/downloads/release/python-350/)

> So far there is only one crawler but I'll add more later hehe :wink:

## Environment
The project was made using Python 3.5 and the following libs:
- beautifulsoup4 (4.6.3)
- pymongo (3.7.1)
- requests (2.19.1)
- urllib3 (1.23)


## User Agent
Module for managing user-agents
You can optionally use mongodb to store data and retrieve from there
Source: [whatismybrowser](https://developers.whatismybrowser.com/useragents/explore/)

### How to use?
```
from modules.useragent import Source

src = Source(filter='operating_system_name', value='windows', limit=500, db_enabled=True)

# upload data to mongo database  
src.update_database()  

# select random user agent  
r = src.random()
```
- **filter**: software_name, operating_system_name, software_type_specific, operating_platform or hardware_type_specific
- **value**: see options accessing `developers.whatismybrowser.com/useragents/explore/FILTER/`
- **limit**: how many user-agents will be in your population/list
- **db_enabled**: whether or not you want to use mongodb to store the list 

### Methods
`get_data()`: Read the source and returns as a JSON or list.
Accepts the parameter **as_json** (True/False) to format the return type.
 ```
[{
   "_id":{
      "$oid":"5b99572c18a3440eefffabfe"
   },
   "created_at":"2018-09-12 18:12:25",
   "agent":"Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; rv:11.0) like Gecko",
   "priority":1
},
...
]
```
`update_database`: Update the data from mongodb. Only works when the parameter **db_enabled** is True. It uses the **browser_useragent** database and the **useragent** collection.
> :bulb: Notice: the database configuration is set on the file `settings/useragent.py`

Returns True if the update was successful or False.

`src.random()`: Selects a random user-agent and returns a JSON or string.
Parameters: any field from the JSON and **as_json** (defaults to True)
Response:
```
{
   "_id":{
      "$oid":"5b99572c18a3440eefffabfe"
   },
   "created_at":"2018-09-12 18:12:25",
   "agent":"Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; rv:11.0) like Gecko",
   "priority":1
}
```
