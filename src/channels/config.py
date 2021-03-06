"""
Channels configuration parameters
"""

ACK = """
We have received your request. We will get back to you shortly.
\n%s
"""
ACK_OTP = """
we have received your request please enter the temporary password we've sent to you.\n%s
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

SQL = {}
SQL['insert_requests'] = "insert into requests (request_id, channel_id, sender_id, request_type, otp_password) values ({request_id}, {channel_id}, {user_id}, '{service_id}', '{otp_code}')"

SERVICES['lotto'] = {}
SERVICES['lotto']['type'] = 'static'
SERVICES['lotto']['text'] = """
Like our facebook page My Lotto Kenya on https://facebook.com/mylottokenya
"""


SERVICES['myluckyday'] = {}
SERVICES['myluckyday']['type'] = 'static'
SERVICES['myluckyday']['text'] = """
Send us your lucky number to 0702123456 and stand a chance to win a Samsung Galaxy S550
"""


SERVICES['jkl'] = {}
SERVICES['jkl']['type'] = 'static'
SERVICES['jkl']['text'] = """
Catch Jeff Koinange Live show every Monday at 8 PM!
"""

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
