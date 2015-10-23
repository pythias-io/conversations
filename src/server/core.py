"""
"""
import time
from commonutils.watson.client import WDSClient
from commonutils.memcache.core import MemcacheHandler
from enttwitter.src.exchange.pub import Publisher

DIALOG_ID = 'b55fae6c-aeef-49af-9b54-98430b3b0e42'
CACHE_ID = 'conversations.id'
REQUESTS_QUEUE = 'enttwtr.twitter.requests'

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
        cache_key = '%s.%s' % (CACHE_ID, str(user_id))
        memcache.set(cache_key, str(conversation_id), 60)

        response = dict(
                conversation_id=conversation_id,
                client_id=text_response['client_id'],
                message=text_response['response'])
        return response

    except AssertionError:
        error = 'initiate_conversation() - AssertionErr: %s' % str(err)
        print error
        raise AssertionError(error)

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
        cache_key = '%s.%s' % (CACHE_ID, str(user_id))
        conversation_id = memcache.get(cache_key)

        payload = dict(dialog_id=DIALOG_ID)
        client = WDSClient(payload)
        conv_response = client.run_conversation(new=False,
                user_input=user_input, conversation_id=conversation_id)
        text_response = eval(conv_response.text)
        print text_response

        response = dict(
                conversation_id=conversation_id,
                client_id=text_response['client_id'],
                message=text_response['response'])
        return response

    except Exception, err:
        error = 'continue_conversation() - %s' % str(err)
        print error
        raise err


def queue_request(resp):
    '''
    Queues dynamic requests for REQUESTS service

    {'conversation_id': '69375',
    'message': ['balance', '', 'Feel free to ask another question... You can request for your account balance or a mini statement. We can even help you locate an ATM near you'],
    'client_id': ***REMOVED***}
    '''
    try:
        payload = {'service_id': resp['action'],
                'username': resp['channel'],
                'user': resp['username'],
                'user_id': resp['client_id'],
                'password': '',
                'request_id': resp['conversation_id'],
                'args': {'channel': resp['channel']}}
        Publisher(payload, REQUESTS_QUEUE)

    except Exception, err:
        error = 'continue_conversation() - %s' % str(err)
        print error
        raise err





