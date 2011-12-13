__doc__="""
gadjo.requestprovider gives you access to the current django HTTPRequest object
whenever you need it without using python's thread locals().

using gadjo.requestprovider
--------------------------

add gadjo's requestprovider middleware to django's settings.py:
MIDDLEWARE_CLASSES=(
'gadjo.requestprovider.middleware.RequestProvider',
...
)

Whenever you need the request object (from your model, form, etc):

from gadjo.requestprovider.signals import get_request

http_request = get_request()


For more infos see the package homepage @pypi

"""
