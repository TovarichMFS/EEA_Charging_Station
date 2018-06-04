#!/usr/bin/env python

import asyncio
import websockets
import random
import time

"""
This program simulates how a charging station can handle connections
-it has to be runned first
-it will run until you kill it
"""

price = 0.2

#Handler of a plug connection
async def handle(websocket, path):
    while True:
	    call = await websocket.recv()
	    #When a car plugs, the station turns itself on occupied and starts the communication
	    if call=='Plugged':
		    print(f"--------------------------------------------")
		    print(f"Station occupied")
		    print(f"--------------------------------------------")
		    resp = f"Connected"
		    await websocket.send(resp)
		    print(f"> {resp}")
		#When a car sends its ID
	    elif call=='ID':
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
		#When a car sends its needs
	    elif call=='Needs':
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
		    #Starts the charging process
		    print(f"--------------------------------------------")
		    resp = f"Charging begins"
		    await websocket.send(resp)
		    print(f"> {resp}")
		    total = 0

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
			    bill = total*price
			    resp = f"{bill}"
			    await websocket.send(resp)
			    print(f"> Billed {bill} $")
		#When the car validates the payment, the transaction ends
	    elif call=='Payed':
		    print(f"< Received")
		    resp = f"End"
		    await websocket.send(resp)
		    print(f"> Transaction ended")
		#When the car asked for the stop of the process
	    elif call=='Stop transaction':
	    	#bills following the amount provided
		    bill = total*price
		    resp = f"{bill}"
		    await websocket.send(resp)
		    print(f"> Billed {bill} $")
		    #Waits for the payment validation and turns itself available
		    call = await websocket.recv()
		    print(f"< {call}")
		    print('< Unplugged')
		    print(f"--------------------------------------------")
		    print(f"Station available, waiting for a customer...")
		    print(f"--------------------------------------------")
		    break
		#When the process is finished, wiats for the car to unplug
	    elif call=='Ended':
		    print("Waiting for unplug")
		#When the car finally unplug, turns itself available
	    elif call=='Unplugged':
		    print('< Unplugged')
		    print(f"--------------------------------------------")
		    print(f"Station available, waiting for a customer...")
		    print(f"--------------------------------------------")
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