#!/usr/bin/env python

import asyncio
import websockets
import random
import time
import datetime
from ocpp_datatypes import *
from ocpp_datatypes_enum import *
import ocpp_messages
from ocpp_messages_parser import *
import authorize_pb2

"""
This program simulates how a charging station can handle connections
-it has to be runned first
-it will run until you kill it
"""

# price = 0.2
powerAmount = 0
total = 0
seqNo = 0
totalSum = 0

evseId = 1
connectorId = 1


def getTime():
	utcTime = datetime.datetime.utcnow()
	localTime = datetime.datetime.now()

	formatTime = '{:d}'.format(localTime.year) + '-' + '{:02d}'.format(localTime.month) + '-' + '{:02d}'.format(
		localTime.day) + 'T' + \
				 '{:02d}'.format(localTime.hour) + ':' + '{:02d}'.format(localTime.minute) + ':' + '{:02d}'.format(
		localTime.second) + \
				 str(localTime.astimezone())[26:]

	return formatTime

async def connect(websocket):
	global seqNo
	async with websockets.connect('ws://localhost:8865') as websocket2:
		resp = "StatusNotification"
		await websocket2.send(resp)
		request = ocpp_messages.statusNotificationRequest(getTime(), ConnectorStatusEnumType.Occupied, evseId, connectorId)
		await websocket2.send(request.SerializeToString())
	print("--------------------------------------------")
	print("Station occupied")
	print("--------------------------------------------")
	async with websockets.connect('ws://localhost:8865') as websocket2:
		resp = "TransactionEvent"
		await websocket2.send(resp)

		seqNo += 1
		transactionData = TransactionType(str(seqNo), ChargingStateEnumType.Charging)
		evse = EVSEType(evseId, connectorId)
		request = ocpp_messages.transactionEventRequest(TransactionEventEnumType.Started, getTime(),
														TriggerReasonEnumType.ChargingStateChanged, seqNo,
														transactionData=transactionData, evse=evse)
		await websocket2.send(request.SerializeToString())
	resp = "Connected"
	await websocket.send(resp)
	print(f"> {resp}")

async def authorize(websocket):
	call = await websocket.recv()
	id = call
	print(f"> ID: {call} received")
	# Verification of the ID (verifies if something has been typed)
	if call != '':
		async with websockets.connect('ws://localhost:8865') as websocket2:
			resp = "Authorize"
			await websocket2.send(resp)
			idToken = IdTokenType(call, IdTokenEnumType.Central)
			request = ocpp_messages.authorizeRequest(idToken=idToken)
			await websocket2.send(request.SerializeToString())
			response = await websocket2.recv()
		response = parse_authorizeResponse(response)
		if authorize_pb2.AuthorizeResponse.CertificateStatusEnumType.Name(response.idTokenInfo.status) == "Accepted":
			resp = "Authorized"
		else:
			resp = "Unauthorized"
	else:
		resp = "Unauthorized"
	print(f"> {resp}")
	if resp == "Unauthorized":
		global seqNo
		async with websockets.connect('ws://localhost:8865') as websocket2:
			response = "TransactionEvent"
			await websocket2.send(response)

			seqNo += 1
			transactionData = TransactionType(str(seqNo), ChargingStateEnumType.SuspendedEVSE)
			evse = EVSEType(evseId, connectorId)
			request = ocpp_messages.transactionEventRequest(TransactionEventEnumType.Ended, getTime(),
															TriggerReasonEnumType.ChargingStateChanged, seqNo,
															transactionData=transactionData, evse=evse)
			await websocket2.send(request.SerializeToString())
	else:
		async with websockets.connect('ws://localhost:8865') as websocket2:
			response = "TransactionEvent"
			await websocket2.send(response)

			seqNo += 1
			transactionData = TransactionType(str(seqNo), ChargingStateEnumType.Charging)
			idToken = IdTokenType(str(id), IdTokenEnumType.Central)
			evse = EVSEType(evseId, connectorId)
			request = ocpp_messages.transactionEventRequest(TransactionEventEnumType.Updated, getTime(),
															TriggerReasonEnumType.ChargingStateChanged, seqNo,
															transactionData=transactionData, idToken=idToken,
															evse=evse)
			await websocket2.send(request.SerializeToString())

			response = await websocket2.recv()
			response = parse_transactionEventResponse(response)
			if transaction_event_pb2.TransactionEventResponse.IdTokenInfoType. \
				AuthorizationStatusEnumType.Name(response.idTokenInfo.status) != "Accepted":
				resp = "Unauthorized"
	await websocket.send(resp)


async def allow(websocket):
	global powerAmount
	global seqNo
	powerAmount = await websocket.recv()
	print(f"> {powerAmount} kWh needed")
	money = await websocket.recv()
	print(f"> {money} $ available")
	# Verifies if the car can pay for the amount of power asked. If it can't, allows the max that can be paid
	# if float(money) - (float(powerAmount) * price) < 0:
	# 	powerAmount = float(money) / price
	resp = f"{powerAmount}"
	await websocket.send(resp)
	print(f"> {resp} kWh allowed")


async def charge(websocket):
	global total
	global seqNo
	global totalSum
	totalSum = 0
	total = 0
	# Starts the charging process
	print(f"--------------------------------------------")
	resp = f"Charging begins"
	await websocket.send(resp)
	print(f"> {resp}")
	# Random amount of power consumed
	consumed = random.randint(1, 80)
	await websocket.send(f"{consumed}")
	print(f"> {consumed} kWh consumed")
	total += consumed
	time.sleep(1)
	# While the amount of power allowed isn't reached
	while total < int(powerAmount):
		call = await websocket.recv()
		print(f"< {call}")
		# if the car validates that she received the previous charge, continues
		if call == 'Received':
			consumed = random.randint(1, 80)
			# Verifies if the amount allowed isn't exceeded else, provides the amount to complete the charge
			if (total + consumed) > int(powerAmount):
				consumed = int(powerAmount) - total
				total = int(powerAmount)
			else:
				total += consumed
			async with websockets.connect('ws://localhost:8865') as websocket2:
				resp = "TransactionEvent"
				await websocket2.send(resp)

				seqNo += 1
				transactionData = TransactionType(str(seqNo), ChargingStateEnumType.Charging)
				evse = EVSEType(evseId, connectorId)
				sampledValue = SampledValueType(Decimal(consumed))
				meterValue = MeterValueType(getTime(), sampledValue)
				request = ocpp_messages.transactionEventRequest(TransactionEventEnumType.Updated, getTime(),
																TriggerReasonEnumType.MeterValuePeriodic, seqNo,
																transactionData=transactionData, evse=evse,
																meterValue=meterValue)
				await websocket2.send(request.SerializeToString())

				response = await websocket2.recv()
				response = parse_transactionEventResponse(response)
				totalSum += Decimal(response.totalCost)


			await websocket.send(f"{consumed}")
			print(f"> {consumed} kWh consumed")
			time.sleep(1)
		# else exits the process
		else:
			total -= consumed
			break
	# If process didn't end normally, starts the stopping process
	if call != 'Received':
		await websocket.send("Stopped")
		print(f"--------------------------------------------")
		print(f"> Charging stopped")
	# else the bill is sent
	else:
		await websocket.send("Complete")
		print(f"--------------------------------------------")
		print(f"> Charging complete")
	await bill(websocket)


async def bill(websocket):
	global total
	global price
	resp = f"{totalSum}"
	await websocket.send(resp)
	print(f"> Billed {totalSum} $")

async def end(websocket):
	global seqNo
	async with websockets.connect('ws://localhost:8865') as websocket2:
		response = "TransactionEvent"
		await websocket2.send(response)
		seqNo += 1
		transactionData = TransactionType(str(seqNo), ChargingStateEnumType.SuspendedEVSE)
		evse = EVSEType(evseId, connectorId)
		request = ocpp_messages.transactionEventRequest(TransactionEventEnumType.Ended, getTime(),
														TriggerReasonEnumType.ChargingStateChanged, seqNo,
														transactionData=transactionData, evse=evse)
		await websocket2.send(request.SerializeToString())
	resp = f"End"
	await websocket.send(resp)
	print(f"> Transaction ended")


async def unplug(websocket):
	async with websockets.connect('ws://localhost:8865') as websocket2:
		resp = "StatusNotification"
		await websocket2.send(resp)
		request = ocpp_messages.statusNotificationRequest(getTime(), ConnectorStatusEnumType.Available, evseId, connectorId)
		await websocket2.send(request.SerializeToString())
	print('< Unplugged')
	print(f"--------------------------------------------")
	print(f"Station available, waiting for a customer...")
	print(f"--------------------------------------------")


# Handler of a plug connection
async def handle(websocket, path):
	while True:
		call = await websocket.recv()
		# When a car plugs, the station turns itself on occupied and starts the communication
		if call == 'Plugged':
			await connect(websocket)
		# When a car sends its ID
		elif call == 'ID':
			await authorize(websocket)
		# When a car sends its needs
		elif call == 'Needs':
			await allow(websocket)
		elif call == 'Start':
			await charge(websocket)
		# When the car validates the payment, the transaction ends
		elif call == 'Payed':
			print(f"< Received")
			resp = f"End"
			await websocket.send(resp)
			print(f"> Transaction ended")
		# When the process is finished, wiats for the car to unplug
		elif call == 'Ended':
			print("Waiting for unplug")
			await end(websocket)
		# When the car finally unplug, turns itself available
		elif call == 'Unplugged':
			await unplug(websocket)
			break


# Starts the local server
start_server = websockets.serve(handle, 'localhost', 8765)
print(f"--------------------------------------------")
print(f"Waiting for a customer...")
print(f"--------------------------------------------")
# Adds the plugging handler
asyncio.get_event_loop().run_until_complete(start_server)
# Asks the server to be an infinite loop
asyncio.get_event_loop().run_forever()
