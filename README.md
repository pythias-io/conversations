# Conversations Engine #

Receives user input from front-end channels

Initiates and maintains conversation sessions between the user and [Watson Dialog Service](https://www.ibm.com/smarterplanet/us/en/ibmwatson/developercloud/doc/dialog/)

All interaction with WDS is through the WDS API wrapper on [commonutils](https://bitbucket.org/pythias_io/commonutils/overview)

## Execution Flow ##

1. Receives HTTP request from channel application (Twitter, Telegram, FB, Whatsapp, etc..)
2. Validate request parameters
3. Initiate dialog (or continue dialog) - depending on request parameters received
4. Receive response from IBM WDS; and match keyword against local config
5. Distinguish static responses from dynamic responses; Publish dynamic responses to SQS queue for Requests engine
6. Publish HTTP response to channel


## :construction: TO DO ##

1. Persist request data on DB
2. Add API authentication mechanisms
3. Add metrics for I/O points

### Services ###

The service runs as a Twisted HTTP listener. Location: 
```
#!bash

conversations/src/server
```

Start service:
```
#!bash
$ twistd -y twistd -y site-conversations.py
```

Stop service:
```
#!bash
$ kill -9 <PID>
```

:bulb: The PID is written to a twistd.pid file every time you start the service

### Endpoints ###

The /conversation? end-point enables the client to initiate and continue conversations.
There are two types of conversations: new and continuing. The type of conversation is inferred from the arguments passed in the HTTP request payload.

New conversation:  To initiate a conversation, the following parameters are required: **USERNAME, USER_ID, CHANNEL**

Continuing conversation:  To keep a conversation going, the following parameters are required:  **USERNAME, USER_ID, CHANNEL, INPUT**

New dialog:

```
#!bash

$ curl -i -X POST --data "username=pythias_io&user_id=***REMOVED***&channel=twitter" "http://***REMOVED***:9010/conversation"
```


Continuing dialog:

```
#!bash

$ curl -i -X POST --data "username=pythias_io&input=give+me+my+balance&user_id=***REMOVED***&channel=twitter" "http://***REMOVED***:9010/conversation"
```

More samples on
```
#!bash

conversations/reference
```



### API Client ###

To test the conversation server, there is a test client at: 
```
#!bash

conversations/src/server/client.py
```

To run the client, invoke it with python and supply a USER_ID as the first argument and USER_INPUT as the second argument. Supply an empty string as USER_INPUT to initiate a new dialog.


```
#!bash

$ python client.py 2 ""
['Hello, welcome to Pythias!']

$ python client.py 2 "what is my balance?"
['You have a CURRENT ACCOUNT a\\/c number *****98801. Your balance is Ksh. 425,901', '', 'Do you have any other questions today?']


```



### :beetle: Bugs ###

1. 
2. 