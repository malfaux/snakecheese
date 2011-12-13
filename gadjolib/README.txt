description
===========

*gadjo.requestprovider* solves the problem of accessing django's HTTPRequest
object whenever is needed, without explicitely passing it down the path of
code.

one of the first solutions was to use python thread's locals() but, 
`as described here`_, this is not so safe. other solutions are available but
those only solve the problem locally.

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
maybe submit it to django-users as a possible contrib. if you find this package
useful, ping their mailing list.

problem references
==================

`accessing request object in a form's clean() method`_

`how to access the request object in admin.py`_

`best way to access request in pre_save`_


.. _as described here: https://code.djangoproject.com/wiki/CookBookThreadlocalsAndUser
.. _accessing request object in a form's clean() method: http://stackoverflow.com/questions/1057252/django-how-do-i-access-the-request-object-or-any-other-variable-in-a-forms-clea
.. _how to access the request object in admin.py: http://stackoverflow.com/questions/727928/django-admin-how-to-access-the-request-object-in-admin-py-for-list-display-meth
.. _best way to access request in pre_save: http://groups.google.com/group/django-users/browse_thread/thread/c859b1ddbdeb917c/e37dbd93db27de84?lnk=raot
