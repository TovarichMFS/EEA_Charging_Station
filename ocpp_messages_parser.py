import authorize_pb2
import status_notification_pb2
import transaction_event_pb2

def parse_statusNotificationRequest(request):
    parsed_request = status_notification_pb2.StatusNotificationRequest()
    parsed_request.ParseFromString(request)
    return parsed_request

def parse_statusNotificationResponse(response):
    parsed_response = status_notification_pb2.StatusNotificationResponse()
    parsed_response.ParseFromString(response)
    return parsed_response


def parse_transactionEventRequest(request):
    parsed_request = transaction_event_pb2.TransactionEventRequest()
    parsed_request.ParseFromString(request)
    return parsed_request

def parse_transactionEventResponse(response):
    parsed_response = transaction_event_pb2.TransactionEventResponse()
    parsed_response.ParseFromString(response)
    return parsed_response

def parse_authorizeRequest(request):
    parsed_request = authorize_pb2.AuthorizeRequest()
    parsed_request.ParseFromString(request)
    return parsed_request

def parse_authorizeResponse(response):
    parsed_response = authorize_pb2.AuthorizeResponse()
    parsed_response.ParseFromString(response)
    return parsed_response