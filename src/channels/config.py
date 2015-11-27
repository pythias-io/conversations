"""
Channels configuration parameters
"""

ACK = """
We have received your request. We will get back to you shortly.
\n%s
"""

SERVICES = {}
SERVICES['options'] = {}

SERVICES['options']['type'] = 'static'
SERVICES['options']['text'] = """
You can check your account balance and request a mini-statement.
We can even help you locate an ATM close to you.
"""

SERVICES['welcome'] = {}
SERVICES['welcome']['type'] = 'static'
SERVICES['welcome']['text'] = """
Hello. Welcome to Pythias. You can request for your balance or a mini-
statement. We can even help you locate an ATM close to you.

Just reply this message with your request.
"""

SERVICES['fail'] = {}
SERVICES['fail']['type'] = 'static'
SERVICES['fail']['text'] = """
I'm sorry. I tried, but could not quite understand your question. Please try again.
"""

SERVICES['balance']= {}
SERVICES['balance']['type'] = 'dynamic'
SERVICES['balance']['action'] = 'balance'

SERVICES['statement'] = {}
SERVICES['statement']['type'] = 'dynamic'
SERVICES['statement']['action'] = 'transactions'


SERVICES['forex'] = {}
SERVICES['forex']['type'] = 'dynamic'
SERVICES['forex']['action'] = 'forex'


SERVICES['buybundle'] = {}
SERVICES['buybundle']['type'] = 'static'
SERVICES['buybundle']['text'] = """
You have successfully purchased the bundle. Your new balance is {balance} MB on your number {user_id}
"""


SERVICES['databalance'] = {}
SERVICES['databalance']['type'] = 'static'
SERVICES['databalance']['text'] = """
You have {balance} MB valid until {day}-{month}-2015 on your number {user_id}
"""
