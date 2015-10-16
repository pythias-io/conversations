# Conversations Engine #

Receives user input from front-end channels

Initiates and maintains conversation sessions between the user and [Watson Dialog Service](https://www.ibm.com/smarterplanet/us/en/ibmwatson/developercloud/doc/dialog/)


### Endpoints ###

New dialog:

```
#!bash

curl -i -X POST --data "user_id=123" "http://***REMOVED***:9010/conversation"
```


Continuing dialog:

```
#!bash

curl -i -X POST --data "user_id=123&input=balance" "http://***REMOVED***:9010/conversation"
```




### How do I get set up? ###

*