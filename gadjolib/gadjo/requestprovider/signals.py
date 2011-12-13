from django.dispatch import Signal

__doc__="""
if you want to get a reference to the current HttpRequest:

from gadjo.requestprovider.signals import get_request
http_request = get_request()

"""
class UnauthorizedSignalReceiver(Exception):
    pass

class SingleHandlerSignal(Signal):

    allowed_receiver='gadjo.requestprovider.middleware.RequestProvider'

    def __init__(self,providing_args = None):
        return Signal.__init__(self,providing_args)

    def connect(self, receiver, sender=None, weak=True, dispatch_uid=None):
        receiver_name = '.'.join([receiver.__class__.__module__,
            receiver.__class__.__name__])
        if receiver_name != self.allowed_receiver:
            raise UnauthorizedSignalReceiver()
        Signal.connect(self, receiver, sender, weak, dispatch_uid)


request_accessor = SingleHandlerSignal()


def get_request():
    return request_accessor.send(None)[0][1]

