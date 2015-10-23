import logging
from logging.handlers import TimedRotatingFileHandler

from twisted.web import http
from twisted.internet import threads

from commonutils.common.core import (verify_params,
        log, MissingParameterException)
from enttwitter.src.configs.register import HTTP

from conversations.src.server.core import (initiate_conversation,
        continue_conversation, queue_request)
from conversations.src.channels.config import SERVICES, ACK


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
            print 'Params: %s' % params
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
        #verify_params(params, ['user_id'])
        assert 'user_id' in params

        print 'new session'
        resp = initiate_conversation(params)

        if 'input' in params:
            if params['input'].isalpha():
                print 'existing session'
                resp = continue_conversation(params)

        print "--- %s ---" % resp
        req_type = SERVICES[resp['message'][0]]['type']
        resp['type'] = req_type
        if req_type == 'static':
            response = SERVICES[resp['message'][0]]['text']
        elif req_type == 'dynamic':
            # queue request
            resp['action'] = SERVICES[resp['message'][0]]['action']
            resp['channel'] = params['channel']
            resp['username'] = params['username']
            queue_request(resp)
            print 'request queued'
            response = ACK % params['user_id']

        resp['user_message'] = response

        write_response(resp, request)

    #except MissingParameterException:
    except AssertionError:
        write_error(request, 'missing_parameter')
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

