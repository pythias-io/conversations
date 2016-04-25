"""
channel client
"""
import sys
import requests

#URL = 'http://52.28.87.96:9010/conversation'
URL = 'http://127.0.0.1:9010/conversation'
DEBUG = False
CHANNEL = 'client.py'
USERNAME = 'client.py'


def log(message, override=False):
    if not override:
        if DEBUG:
            print message
    else:
        print message

def start_dialog(user_id):
    try:
        dialog = requests.post(URL,
                data={'user_id': user_id, 'channel': CHANNEL, 'username': USERNAME})
        log("%s: %s" % (dialog.status_code, dialog.text))
        log(dialog.text, override=True)

    except Exception, err:
        log('start_dialog: %s' % err)
        raise err


def continue_dialog(user_id, user_input):
    try:
        dialog = requests.post(URL,
                data={'input': user_input, 'user_id': user_id, 'channel': CHANNEL, 'username': USERNAME})
        log("%s: %s" % (dialog.status_code, dialog.text))
        log(dialog.text, override=True)

    except Exception, err:
        log('continue_dialog: %s' % err)
        raise err

if __name__ == '__main__':
    user_id = str(sys.argv[1])
    user_input = str(sys.argv[2])

    log("userID: %s | userInput: %s" % (user_id, user_input))
    if len(user_input) > 0:
        # continuing dialog
        log("ongoing dialog | user_id: %s" % user_id)
        continue_dialog(user_id, user_input)
    else:
        # new dialog
        log("new dialog %s" % user_id)
        start_dialog(user_id)
