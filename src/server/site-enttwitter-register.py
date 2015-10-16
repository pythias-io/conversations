#!/usr/bin/python2.7
from twisted.application import internet, service
from twisted.web import server, resource
from conversations.src.server.server import RequestFactory
from twisted.python.log import ILogObserver, FileLogObserver
from twisted.python.logfile import DailyLogFile
from twisted.internet import reactor
port = 9010
threads = 20
log = 'log-twistd-conversation-server.log'

ProfilerService = internet.TCPServer(port, RequestFactory())
ProfilerService.setName('enttwitter-register-http')
application = service.Application('enttwitter-register-http')
ProfilerService.setServiceParent(application)
logfile = DailyLogFile('%s' % log, 'logs/')
application.setComponent(ILogObserver, FileLogObserver(logfile).emit)
reactor.suggestThreadPoolSize(threads)
