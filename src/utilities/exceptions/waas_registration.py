# The class NoMessageInQueueError is a custom exception class that represents an
# error when there is no message in a queue.
class NoMessageInQueueError(Exception):
    pass


# The class RequestNotSentT0KCBError is a custom exception that can be raised when
# a request is not sent to the KCB API.
class RequestNotSentT0KCBError(Exception):
    pass
