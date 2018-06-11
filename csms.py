#!/usr/bin/env python

import asyncio
import websockets

#Handler of a plug connection
async def handle(websocket, path):
    call = await websocket.recv()
    await websocket.send("Hello")
    # while True:
	 #    call = await websocket.recv()
	 #    #When a car plugs, the station turns itself on occupied and starts the communication
	 #    if call=='Plugged':
		#     await connect(websocket)
		# #When a car sends its ID
	 #    elif call=='ID':
		#     await authorize(websocket)
		# #When a car sends its needs
	 #    elif call=='Needs':
		#     await allow(websocket)
	 #    elif call=='Start':
		#     await charge(websocket)
		# #When the car validates the payment, the transaction ends
	 #    elif call=='Payed':
		#     print(f"< Received")
		#     resp = f"End"
		#     await websocket.send(resp)
		#     print(f"> Transaction ended")
		# #When the process is finished, wiats for the car to unplug
	 #    elif call=='Ended':
		#     print("Waiting for unplug")
		# #When the car finally unplug, turns itself available
	 #    elif call=='Unplugged':
		#     await unplug(websocket)
		#     break

#Starts the local server
start_server = websockets.serve(handle, 'localhost', 8865)
print(f"--------------------------------------------")
print(f"Waiting for a charging station...")
print(f"--------------------------------------------")
#Adds the plugging handler
asyncio.get_event_loop().run_until_complete(start_server)
#Asks the server to be an infinite loop
asyncio.get_event_loop().run_forever()