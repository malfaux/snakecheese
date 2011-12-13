quickie
======
+ installation: easy-install django-contrib-requestprovider
+ pypi_home: http://pypi.python.org/pypi?name=django-contrib-requestprovider&version=1.0.1&:action=display

description
===========

*gadjo.requestprovider* gives access to django's HTTPRequest
object whenever is needed, without explicitly passing it down the path of
code.

usage
=====

add gadjo's requestprovider middleware to django's settings.py:

MIDDLEWARE_CLASSES=(
'gadjo.requestprovider.middleware.RequestProvider',
...
)

Whenever you need the request object (from your model, form, etc):

from gadjo.requestprovider.signals import get_request

http_request = get_request()


implementation details
======================

besides saving a reference to the current request, the RequestProvider
middleware also registers itself as a receiver for whoever signals that it
needs the request object. 

whenver a get_request() is issued, the middleware is called to process the
signal and returns the request object. 
this works because the signals in django are processed synchronously. 
get_request() calls send() on the request_accessor SingleHandlerSignal(Signal)
object and returns the current request to the caller.
A SingleHandlerSignal is a Signal that makes sure it will only register
authorized receivers. This is to make sure no one will register a handler
(maybe by mistake) for a request_accessor signal since this is supposed to be
handled only by our RequestProvider middleware.

class SingleHandlerSignal(Signal):

    allowed_receiver='gadjo.requestprovider.middleware.RequestProvider'


the Signal's connect() method is overwritten to register only allowed
receivers.



TODO
====
nothin


NOTE
====
this is not thread-safe. however, if you are running your django apps in a threaded environment
I don't think you really know what you're doing.
