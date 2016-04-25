"""
"""
import os
import json
import time
from db_utilities.mysql.core import run_query

from commonutils.common.core import log
from commonutils.watson.client import WDSClient
from commonutils.memcache.core import MemcacheHandler
from service_engine.src.configs.config import SQS_CONFIG,SQL
from persistence_manager.src.consumer.client import publish, get_response

import boto3

<<<<<<< HEAD
DIALOG_ID = os.getenv('DIALOG_ID')
=======
DIALOG_ID = '0953ab97-2e85-4968-8bc1-f906f23622f3'
>>>>>>> origin/ktn-demo
CACHE_ID = 'conversations.id'

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
        print "WDS Response for {user_id} - {request_id} : %s".format(
                **params) % text_response
        conversation_id = text_response['conversation_id']
        client_id = text_response['client_id']
        assert str(client_id) == str(user_id)

        memcache = MemcacheHandler()
        cache_key = '%s.%s' % (CACHE_ID, str(user_id))
        memcache.set(cache_key, str(conversation_id), 300)

        response = dict(
                conversation_id=conversation_id,
                client_id=text_response['client_id'],
                message=text_response['response'])
        return response

    except AssertionError:
        error = 'ERROR: initiate_conversation() - client_id and user_id do not match'
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
        print 'conversation ID from cache %s' % conversation_id

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
    Publishes request payload to SQS for REQUESTS service to consume

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

        sqs_client = boto3.client(
                'sqs',
                aws_access_key_id=SQS_CONFIG.get('access_key'),
                aws_secret_access_key=SQS_CONFIG.get('secret'),
                region_name=SQS_CONFIG.get('region')
                )
        queue = SQS_CONFIG['requests_queue']
        published = sqs_client.send_message(
                QueueUrl=queue,
                MessageBody=json.dumps(payload)
                )
        log('Published msg %s to queue %s -- %s' % (
            published.get('MessageId'), queue, resp), 'info')

    except Exception, err:
        error = 'continue_conversation() - %s' % str(err)
        log(error, 'error')
        raise err


def is_verified(params):
    '''

    {'message': ((0,),), 'rows': 1, 'ok': True}

    {'message': (), 'rows': 0, 'ok': True}

    '''
    try:
        verified, not_verified = 1, 0
        channel = params['channel']
        if channel.lower() == 'twitter':
            query = "select verified from twitter_users where twitter_id = {}".format(params['user_id'])
            resp = run_query(query)
            log('Verified: DB resp: {}'.format(str(resp)), 'debug')
            if resp['ok'] and resp['message']:
                verif = resp['message'][0][0]
                return True if verif == verified else False
            else:
                return False

        
        else:
            return True

    except Exception, err:
        log('is_verified() - {} -- {}'.format(str(err), params), 'error')
        raise err

def insert(params):
    '''
    inserts OTP requests in a db 
    '''
    try:
        channel_id = params['channel']
        #publish to persistance queue
        publish(params['request_id'], SQL['insert_requests'])
        #fetch
        x = 0
        resp = None
        while x < 4:
            resp = get_reponse(params['request_id'])
            if eval(resp):
                break
            sleep(0.01)
            x += 1
        log('%s - DB Insert resp: %s -- %s' % (str(x), resp,
            params['request_id']), 'debug', logger)
    
    except Exception, err:
        log('insert fail- %s --%s' %(str(err),'error',self.logger))
