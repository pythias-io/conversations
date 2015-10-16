"""
"""
import time
from commonutils.watson.client import WDSClient
from commonutils.memcache.core import MemcacheHandler

DIALOG_ID = '005c3873-680f-437b-94a9-83ee7fe54569'

def initiate_conversation(params):
    '''
    '''
    try:
        now = int(time.time())
        user_id = str(params['user_id'])
        payload = dict(user_id=params['user_id'], dialog_id=DIALOG_ID)
        client = WDSClient(payload)
        ini_response = client.run_conversation(new=True)
        text_response = eval(ini_response.text)
        print text_response
        conversation_id = text_response['conversation_id']
        client_id = text_response['client_id']
        assert str(client_id) == str(user_id)

        memcache = MemcacheHandler()
        memcache.set(str(user_id), str(conversation_id), 60)

        response = text_response['response']
        return response

    except AssertionError:
        error = 'initiate_conversation() - AssertionErr: %s' % str(err)
        print error
        raise err

    except Exception, err:
        error = 'initiate_conversation() - %s' % str(err)
        print error
        raise err


def continue_conversation(params):
    '''
    '''
    try:
        user_id = params['user_id']
        user_input = params['input']

        memcache = MemcacheHandler()
        conversation_id = memcache.get(str(user_id))

        payload = dict(dialog_id=DIALOG_ID)
        client = WDSClient(payload)
        conv_response = client.run_conversation(new=False,
                user_input=user_input, conversation_id=conversation_id)
        text_response = eval(conv_response.text)
        print text_response

        response = text_response['response']
        return response

    except Exception, err:
        error = 'continue_conversation() - %s' % str(err)
        print error
        raise err
