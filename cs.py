#!/usr/bin/env python

import asyncio
import websockets
import random
import time

price = 0.2

async def handle(websocket, path):
    while True:
	    call = await websocket.recv()
	    if call=='Plugged':
		    resp = f"Connected"
		    await websocket.send(resp)
		    print(f"> {resp}")
	    elif call=='ID':
		    call = await websocket.recv()
		    print(f"> ID: {call} received")
		    if call!='':
			    resp = f"Authorized"
			    await websocket.send(resp)
			    print(f"> {resp}")
		    else:
			    resp = f"Unauthorized"
			    await websocket.send(resp)
			    print(f"> {resp}")
	    elif call=='Needs':
		    powerAmount = await websocket.recv()
		    print(f"> {powerAmount} kWh needed")
		    money = await websocket.recv()
		    print(f"> {money} $ available")
		    if float(money) - (float(powerAmount)*price) < 0:
			    powerAmount = float(money)/price

		    resp = f"{powerAmount}"
		    await websocket.send(resp)
		    print(f"> {resp} kWh allowed")
		    resp = f"Charging begins"
		    await websocket.send(resp)
		    print(f"> {resp}")
		    total = 0

		    consumed = random.randint(1,80)
		    await websocket.send(f"{consumed}")
		    print(f"> {consumed} kWh consumed")
		    total += consumed
		    time.sleep(1)
		    while total<int(powerAmount):
			    call = await websocket.recv()
			    print(f"< {call}")
			    if call=='Received':
				    consumed = random.randint(1,80)
				    if (total+consumed)>int(powerAmount):
					    consumed = int(powerAmount) - total
					    total = int(powerAmount)
				    else:
					    total += consumed
				    await websocket.send(f"{consumed}")
				    print(f"> {consumed} kWh consumed")
				    time.sleep(1)
			    else:
				    break

		    if call!='Received':
			    await websocket.send("Stopped")
			    print(f"> Charging stopped")
		    else:
			    await websocket.send("Complete")
			    print(f"> Charging complete")
			    bill = total*price
			    resp = f"{bill}"
			    await websocket.send(resp)
			    print(f"> Billed {bill} $")
	    elif call=='Payed':
		    print(f"< Received")
		    resp = f"End"
		    await websocket.send(resp)
		    print(f"> Transaction ended")
	    elif call=='Stop transaction':
		    bill = total*price
		    resp = f"{bill}"
		    await websocket.send(resp)
		    print(f"> Billed {bill} $")
		    call = await websocket.recv()
		    print(f"< {call}")
		    print('< Unplugged')
		    break
	    elif call=='Ended':
		    print("Waiting for unplug")
	    elif call=='Unplugged':
		    print('< Unplugged')
		    break

start_server = websockets.serve(handle, 'localhost', 8765)

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()