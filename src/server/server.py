import logging
import random
from logging.handlers import TimedRotatingFileHandler

from twisted.web import http
from twisted.internet import threads
from commonutils.common.core import (verify_params,
        log, MissingParameterException)
from enttwitter.src.configs.register import HTTP

from conversations.src.server.core import (initiate_conversation,
        continue_conversation, queue_request, is_verified,insert)
from conversations.src.channels.config import SERVICES, ACK , ACK_OTP

def get_params(request):
    '''
    retrieve request params and add to dict
    '''
    try:
        params = {}
        for key, val in request.args.items():
            params[key] = val[0]
        log('request params - %s' % params, 'debug')
        return params
    except Exception, err:
        log('get_params() fail - %r' % err, 'error')
        raise err


def write_response(response, request):
    '''
    write http response
    '''
    try:
        request.setHeader('X-Status', 'success')
        request.setHeader('X-ConversationId',
                response.get('conversation_id'))
        request.setHeader('X-ClientId',
                response.get('client_id'))
        request.setHeader('X-RequestType',
                response.get('type'))
        request.write(str(response['user_message']))
        request.finish()
    except Exception, err:
        log('write_response() fail - %r' % err, 'error')
        write_error(request, 'error')


def write_error(request, error):
    '''
    write error on http response
    '''
    try:
        request.setHeader('X-Status', 'error')
        request.write(str(error))
        request.finish()
    except Exception, err:
        log('write_error() fail - %r' % err, 'error')
        return

def publish_request(msg):
    '''
    publish request to queue for consumer
    '''
    pass

def setup(func):
    '''
    decorator that extracts http parameters
    from requests object and adds them to `params` dict

    '''
    def __inner(request):
        try:
            params = get_params(request)
            func(params, request)
        except Exception, err:
            error = 'setup() fail - %r' % err
            log(error, 'error')
            raise err
    return __inner

@setup
def process_conversation(params, request):
    '''
    '''
    try:
        # validate parameters
        exc = 'missing parameter'
        for mandatory in ['user_id', 'channel']:
            assert mandatory in params

        # check user's registration and verification status
        exc = 'verification_fail'
        assert is_verified(params)

        new = True
        numerical = False
       #check if its an otp or wds request
        if 'input' in params:
            if len(str(params['input'])) > 1:
                new = False
            if (params['input']).isdigit():
                numerical = True

        if numerical == True:
            print 'publishing to OTP input:%s'
            otp_code = random.randint(999,10000)
            params['otp_code'] = otp_code
            response = ACK_OTP % params['user_id']
                
                #calls the OTP engine#
                #                    #
                ######################
                #insert(params)
        else:
            if new == True:
                print 'new session'
                resp = initiate_conversation(params)
            else:
                print 'existing session'
                resp = continue_conversation(params)
            
            try:
                req_type = SERVICES[resp['message'][0]]['type']
                print 'Request type: %s -- %s' % (req_type, params)
            except KeyError:
                err = 'ERROR: Service not defined - %s' % params
                raise Exception(err)
            
            resp['type'] = req_type
            if req_type == 'static':
                response = SERVICES[resp['message'][0]]['text']
            elif req_type == 'dynamic':
                #check if its an otp request
                if 'message' in resp:
                    if SERVICES[resp['message'][0]['action']] == 'balance' or SERVICES[resp['message'][0]['action']] == 'transactions':
                            print 'calling the otp engine'
                            #############
                            # otp engine
                            #############
                    else:
                        #queue request
                        resp['action'] = SERVICES[resp['message'][0]]['action']
                        resp['channel'] = params['channel']
                        resp['username'] = params['username']
                        queue_request(resp)
                        response = ACK % params['user_id']
                
        resp['user_message'] = response
            
        write_response(resp, request)

    #except MissingParameterException:
    except AssertionError:
        if exc == 'verification_fail':
            resp = {
                    'type': 'static',
                    'user_message': 'You are not registered to use this service'
                    }
            write_response(resp, request)
        
        
        else:
            write_error(request, exc)
            return

    except Exception, err:
        log('process_conversation() fail - %r' % err, 'error')
        write_error(request, 'error')


def get_pages():
    '''
    returns mapping of endpoint : process function
    '''
    return {'/conversation': process_conversation}


def catch_error(*args):
    for arg in args:
        log('error from deffered - %r' % arg, 'error')
    return 'system error'


class requestHandler(http.Request):

    pages = get_pages()

    def __init__(self, channel, queued):
        http.Request.__init__(self, channel, queued)

    def process(self):
        if self.path in self.pages:
            handler = self.pages[self.path]
            d = threads.deferToThread(handler, self)
            d.addErrback(catch_error)
            return d
        else:
            self.setResponseCode(http.NOT_FOUND)
            self.write('404 - page not found')
            self.finish()

class requestProtocol(http.HTTPChannel):
    requestFactory = requestHandler

class RequestFactory(http.HTTPFactory):
    protocol = requestProtocol
    isLeaf = True

    def __init__(self):
        http.HTTPFactory.__init__(self)

