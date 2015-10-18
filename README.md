# Conversations Engine #

Receives user input from front-end channels

Initiates and maintains conversation sessions between the user and [Watson Dialog Service](https://www.ibm.com/smarterplanet/us/en/ibmwatson/developercloud/doc/dialog/)


### Endpoints ###

New dialog:

```
#!bash

$ curl -i -X POST --data "user_id=123" "http://***REMOVED***:9010/conversation"
```


Continuing dialog:

```
#!bash

$ curl -i -X POST --data "user_id=123&input=balance" "http://***REMOVED***:9010/conversation"
```


### API Client ###

To test the conversation server, there is a test client at: 
```
#!bash

/conversations/src/server/client.py
```

To run the client, invoke it with python and supply a USER_ID as the first argument and USER_INPUT as the second argument. Supply an empty string as USER_INPUT to initiate a new dialog.


```
#!bash

$ python client.py 2 ""
['Hello, welcome to Pythias!']

$ python client.py 2 "what is my balance?"
['You have a CURRENT ACCOUNT a\\/c number *****98801. Your balance is Ksh. 425,901', '', 'Do you have any other questions today?']


```



### How do I get set up? ###

*