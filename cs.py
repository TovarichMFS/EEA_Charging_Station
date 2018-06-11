#!/usr/bin/env python

import asyncio
import websockets
import random
import time
import datetime

"""
This program simulates how a charging station can handle connections
-it has to be runned first
-it will run until you kill it
"""

price = 0.2
powerAmount = 0
total = 0

async def connect(websocket):
    print(f"--------------------------------------------")
    print(f"Station occupied")
    print(f"--------------------------------------------")
    resp = f"Connected"
    async with websockets.connect('ws://localhost:8865') as websocket2:
        await websocket2.send("Hey")
        res = await websocket2.recv()
        print(res)
    await websocket.send(resp)
    print(f"> {resp}")

async def authorize(websocket):
    call = await websocket.recv()
    print(f"> ID: {call} received")
    #Verification of the ID (verifies if something has been typed)
    if call!='':
	    resp = f"Authorized"
	    await websocket.send(resp)
	    print(f"> {resp}")
    else:
	    resp = f"Unauthorized"
	    await websocket.send(resp)
	    print(f"> {resp}")

async def allow(websocket):
    global powerAmount
    powerAmount = await websocket.recv()
    print(f"> {powerAmount} kWh needed")
    money = await websocket.recv()
    print(f"> {money} $ available")
    #Verifies if the car can pay for the amount of power asked. If it can't, allows the max that can be paid 
    if float(money) - (float(powerAmount)*price) < 0:
	    powerAmount = float(money)/price
    resp = f"{powerAmount}"
    await websocket.send(resp)
    print(f"> {resp} kWh allowed")

async def charge(websocket):
    global total
    total = 0
    #Starts the charging process
    print(f"--------------------------------------------")
    resp = f"Charging begins"
    await websocket.send(resp)
    print(f"> {resp}")
    #Random amount of power consumed
    consumed = random.randint(1,80)
    await websocket.send(f"{consumed}")
    print(f"> {consumed} kWh consumed")
    total += consumed
    time.sleep(1)
    #While the amount of power allowed isn't reached
    while total<int(powerAmount):
	    call = await websocket.recv()
	    print(f"< {call}")
	    #if the car validates that she received the previous charge, continues
	    if call=='Received':
		    consumed = random.randint(1,80)
		    #Verifies if the amount allowed isn't exceeded else, provides the amount to complete the charge
		    if (total+consumed)>int(powerAmount):
			    consumed = int(powerAmount) - total
			    total = int(powerAmount)
		    else:
			    total += consumed
		    await websocket.send(f"{consumed}")
		    print(f"> {consumed} kWh consumed")
		    time.sleep(1)
		#else exits the process
	    else:
		    total -= consumed
		    break
	#If process didn't end normally, starts the stopping process
    if call!='Received':
	    await websocket.send("Stopped")
	    print(f"--------------------------------------------")
	    print(f"> Charging stopped")
	#else the bill is sent
    else:
	    await websocket.send("Complete")
	    print(f"--------------------------------------------")
	    print(f"> Charging complete")
    await bill(websocket)
	    

async def bill(websocket):
    global total
    global price
    bill = total*price
    resp = f"{bill}"
    await websocket.send(resp)
    print(f"> Billed {bill} $")

async def end(websocket):
    resp = f"End"
    await websocket.send(resp)
    print(f"> Transaction ended")

async def unplug(websocket):
    print('< Unplugged')
    print(f"--------------------------------------------")
    print(f"Station available, waiting for a customer...")
    print(f"--------------------------------------------")
    

#Handler of a plug connection
async def handle(websocket, path):
    while True:
	    call = await websocket.recv()
	    #When a car plugs, the station turns itself on occupied and starts the communication
	    if call=='Plugged':
		    await connect(websocket)
		#When a car sends its ID
	    elif call=='ID':
		    await authorize(websocket)
		#When a car sends its needs
	    elif call=='Needs':
		    await allow(websocket)
	    elif call=='Start':
		    await charge(websocket)
		#When the car validates the payment, the transaction ends
	    elif call=='Payed':
		    print(f"< Received")
		    resp = f"End"
		    await websocket.send(resp)
		    print(f"> Transaction ended")
		#When the process is finished, wiats for the car to unplug
	    elif call=='Ended':
		    print("Waiting for unplug")
		#When the car finally unplug, turns itself available
	    elif call=='Unplugged':
		    await unplug(websocket)
		    break

#Starts the local server
start_server = websockets.serve(handle, 'localhost', 8765)
print(f"--------------------------------------------")
print(f"Waiting for a customer...")
print(f"--------------------------------------------")
#Adds the plugging handler
asyncio.get_event_loop().run_until_complete(start_server)
#Asks the server to be an infinite loop
asyncio.get_event_loop().run_forever()

def getTime():
	utcTime = datetime.datetime.utcnow()
	localTime = datetime.datetime.now()

	formatTime = '{:d}'.format(localTime.year) + '-' + '{:02d}'.format(localTime.month) + '-' + '{:02d}'.format(localTime.day) + 'T' + \
				 '{:02d}'.format(localTime.hour) + ':' + '{:02d}'.format(localTime.minute) + ':' + '{:02d}'.format(localTime.second) +\
				 str(localTime.astimezone())[26:]

	return formatTime

# print(getTime())