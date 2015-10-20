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
