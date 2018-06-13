#!/usr/bin/env python

import asyncio
import websockets
from ocpp_datatypes import *
import ocpp_messages
from ocpp_messages_parser import *

stationsStatus = dict()
price = 0.2


# Handler of a plug connection
async def handle(websocket, path):
    call = await websocket.recv()

    if call == "StatusNotification":
        await statusNotification(websocket)
    elif call == "Authorize":
        await authorize(websocket)
    elif call == "TransactionEvent":
        await transactionEvent(websocket)


async def authorize(websocket):
    call = await websocket.recv()
    request = parse_authorizeRequest(call)
    print(f"> AuthorizeRequest: \n{request}")

    # Need to make a function which check authorization status for given Id
    idTokenInfo = IdTokenInfoType(AuthorizationStatusEnumType.Accepted)
    resp = ocpp_messages.authorizeResponse(idTokenInfo=idTokenInfo)
    print(f"< AuthorizeResponse: \n{resp}")
    await websocket.send(resp.SerializeToString())

async def statusNotification(websocket):
    call = await websocket.recv()
    request = parse_statusNotificationRequest(call)
    print(f"> StatusNotificationRequest: \n{request}")
    status = status_notification_pb2.StatusNotificationRequest.ConnectorStatusEnumType.Name(request.connectorStatus)
    stationsStatus[f"{request.evseId}_{request.connectorId}"] = status

async def transactionEvent(websocket):
    call = await websocket.recv()
    request = parse_transactionEventRequest(call)
    print(f"> TransactionEventRequest: \n{request}")
    eventType = transaction_event_pb2.TransactionEventRequest.TransactionEventEnumType.Name(request.eventType)
    if eventType == "Updated" and request.HasField("idToken"):
        idTokenInfo = IdTokenInfoType(AuthorizationStatusEnumType.Accepted)
        resp = ocpp_messages.transactionEventResponse(idTokenInfo=idTokenInfo)
        print(f"< TransactionEventResponse: \n{resp}")
        await websocket.send(resp.SerializeToString())
    elif eventType == "Updated":
        totalCost = Decimal(price)*Decimal(request.meterValue.sampledValue.value)
        resp = ocpp_messages.transactionEventResponse(totalCost=totalCost)
        print(f"< TransactionEventResponse: \n{resp}")
        await websocket.send(resp.SerializeToString())


# Starts the local server
start_server = websockets.serve(handle, 'localhost', 8865)
print(f"--------------------------------------------")
print(f"Waiting for a charging station...")
print(f"--------------------------------------------")
# Adds the plugging handler
asyncio.get_event_loop().run_until_complete(start_server)
# Asks the server to be an infinite loop
asyncio.get_event_loop().run_forever()
