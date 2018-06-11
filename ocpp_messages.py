import json
from decimal import *
from ocpp_datatypes import *
from ocpp_datatypes_enum import *
from ocpp_datatype_parser import *
import status_notification_pb2

getcontext().prec = 6

def statusNotificationRequest(
        timestamp: str,
        connectorStatus: ConnectorStatusEnumType,
        evseId: int,
        connectorId: int):
    request = status_notification_pb2.StatusNotificationRequest()
    request.timestamp = timestamp
    # print(status_notification_pb2.StatusNotificationRequest.Available)
    if connectorStatus.value == "Available":
        request.connectorStatus = status_notification_pb2.StatusNotificationRequest.Available
    elif connectorStatus.value == "Occupied":
        request.connectorStatus = status_notification_pb2.StatusNotificationRequest.Occupied
    elif connectorStatus.value == "Reserved":
        request.connectorStatus = status_notification_pb2.StatusNotificationRequest.Reserved
    elif connectorStatus.value == "Unavailable":
        request.connectorStatus = status_notification_pb2.StatusNotificationRequest.Unavailable
    elif connectorStatus.value == "Faulted":
        request.connectorStatus = status_notification_pb2.StatusNotificationRequest.Faulted
    request.evseId = evseId
    request.connectorId = connectorId
    return request

    # request = {"type": "StatusNotificationRequest",
    #            "args": {"timestamp": timestamp, "connectorStatus": connectorStatus.value,
    #                     "evseId": evseId, "connectorId": connectorId}}
    # return json.dumps(request)

def statusNotificationResponse():
    response = status_notification_pb2.StatusNotificationResponse()
    return response

    # response = {"type": "StatusNotificationResponse", "args": {}}
    # return json.dumps(response)

def transactionEventRequest(
        eventType: TransactionEventEnumType,
        timestamp: str,
        triggerReason: TriggerReasonEnumType,
        seqNo: int,
        offline: bool = None,
        numberOfPhasesUsed: int = None,
        cableMaxCurrent: Decimal = None,
        reservationId: int = None,
        transactionData: TransactionType = None, # is required
        idToken: IdTokenType = None,
        evse: EVSEType = None,
        meterValue: MeterValueType = None
):
    transactionDataParsed = parse_TransactionType(transactionData)
    idTokenParsed = parse_IdTokenType(idToken)
    evseParsed = parse_EVSEType(evse)
    meterValueParsed = parse_MeterValueType(meterValue)

    # request = {"type": "TransactionEventRequest", "args": {"eventType": eventType.value, "timestamp": timestamp,
    #                                                        "triggerReason": triggerReason.value, "seqNo": seqNo,
    #                                                        "offline": offline, "numberOfPhasesUsed": numberOfPhasesUsed,
    #                                                        "cableMaxCurrent": cableMaxCurrent, "reservationId": reservationId,
    #                                                        "transactionData": transactionDataParsed, "idToken": idTokenParsed,
    #                                                        "evse": evseParsed, "meterValue": meterValueParsed}}
    # return json.dumps(request)

# print(transactionEventRequest(TransactionEventEnumType.Started, "134", TriggerReasonEnumType.Authorized, 1, transactionData=TransactionType(2)))
timestamp = "124"
connectorStatus = ConnectorStatusEnumType.Available
evseId = 2
connectorId = 1
request = statusNotificationRequest(timestamp, connectorStatus, evseId, connectorId)
print(request)
print(statusNotificationResponse())










# import addressbook_pb2
# person = addressbook_pb2.Person()
# person.id = 1234
# person.name = "John Doe"
# person.email = "jdoe@example.com"
# phone = person.phones.add()
# phone.number = "555-4321"
# phone.type = addressbook_pb2.Person.HOME
# a = person.SerializeToString()
# b = addressbook_pb2.Person()
# print(b)
# b.ParseFromString(a)