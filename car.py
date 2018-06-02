#!/usr/bin/env python

import asyncio
import websockets
import signal

batteryCapacity = 500
quit = False

def signal_handler(signal,frame):
		global quit
		quit = True

async def plug():
	step = 0
	battery = 123
	money = 500.0
	totalConsumed = 0
	print(battery)
	async with websockets.connect('ws://localhost:8765') as websocket:
		while step!=-1:
			if quit==False:
				if step==0:
					await websocket.send(f"Plugged")
					print(f"> Plugged")
					step += 1
				elif step==1:
					resp = await websocket.recv()
					print(f"< {resp}")
					if resp=='Connected':
						await websocket.send(f"ID")
						id = input("Enter your ID:")
						await websocket.send(f"{id}")
						print(f"> ID sent")
						step += 1
				elif step==2:
					resp = await websocket.recv()
					print(f"< {resp}")

					if resp=='Authorized':
						needed = batteryCapacity - battery
						await websocket.send(f"Needs")
						await websocket.send(f"{needed}")
						print(f"> Charging request sent")
						await websocket.send(f"{money}")
						print(f"> Money balance sent")

						resp = await websocket.recv()
						print(f"< {resp} kWh allowed")
						step += 1
					else:
						await websocket.send("Ended")
						step = 5
				elif step==3:
					resp = await websocket.recv()
					print(f"< {resp}")
					if resp=='Charging begins':
						resp = await websocket.recv()
						while resp!='Complete' and quit==False:
							print(f"> {resp} kWh consumed")
							await websocket.send(f"Received")
							battery += int(resp)
							totalConsumed += int(resp)
							resp = await websocket.recv()
						step += 1
				elif step==4:
					bill = await websocket.recv()
					print(f"> {bill} $ to pay")
					money -= float(bill)
					await websocket.send("Payed")
					print(f"> Payed")
					print("Balance :"+str(money)+" $")
					resp = await websocket.recv()
					print(f"> {resp}")
					await websocket.send("Ended")
					step += 1
				elif step==5:
					print("Unplug required")
					step += 1
				elif step==-1:
					exit(0)
			else:
				if step!=6:
					await websocket.send("Stop")
					print('Stopping...')
					print(f"> {resp} kWh consumed")
					await websocket.send(f"Received")
					battery += int(resp)
					totalConsumed += int(resp)
					print(totalConsumed)
					resp = await websocket.recv()
					print(f"> {resp}")
					await websocket.send("Stop transaction")
					bill = await websocket.recv()
					print(f"> {bill} $ to pay")
					money -= float(bill)
					await websocket.send("Payed")
					print(f"> Payed")
					print("Balance :"+str(money)+" $")
				else:
					await websocket.send("Unplugged")
				step=-1
				print('> Unplugged')

signal.signal(signal.SIGINT, signal_handler)
asyncio.get_event_loop().run_until_complete(plug())