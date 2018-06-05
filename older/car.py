#!/usr/bin/env python

import asyncio
import websockets
import signal

"""
This program simulates the communication on the side of the car:
- launching this simulates the plugging
- sending SIGINT signal during the program simulates the unplugging/asks for the unplugging
"""

batteryCapacity = 500
quit = False

#Handler for the SIGINT signal
def signal_handler(signal,frame):
		global quit
		quit = True

async def plug():
	step = 0
	battery = 123
	money = 500.0
	async with websockets.connect('ws://localhost:8765') as websocket:
		#step -1 is the ending step
		while step!=-1:
			#if the car doesn't ask the end of the exchange, it will continue
			if quit==False:
				#First contact with the station
				if step==0:
					await websocket.send(f"Plugged")
					print(f"> Plugged")
					step += 1
				#Verification of the connection and sending of credentials
				elif step==1:
					resp = await websocket.recv()
					print(f"< {resp}")
					if resp=='Connected':
						#Warn the station that the credentials will be sent
						await websocket.send(f"ID")
						#Waits for the user to enter an ID
						id = input("Enter your ID:")
						await websocket.send(f"{id}")
						print(f"> ID sent")
						step += 1
				#Verify the authorization and send its needs
				elif step==2:
					resp = await websocket.recv()
					print(f"--------------------------------------------")
					print(f"< {resp}")

					if resp=='Authorized':
						#Amount of power needed
						needed = batteryCapacity - battery
						await websocket.send(f"Needs")
						await websocket.send(f"{needed}")
						print(f"> Charging request sent")
						#Amount of money that can be provided
						await websocket.send(f"{money}")
						print(f"> Money balance sent")

						#Waits for the amount of power allowed by the station
						resp = await websocket.recv()
						print(f"< {resp} kWh allowed")
						step += 1
					else:
						#If unauthorized, the car ends the transaction
						await websocket.send("Ended")
						step = 5
				#Charging process
				elif step==3:
					resp = await websocket.recv()
					print(f"--------------------------------------------")
					print(f"< {resp}")
					if resp=='Charging begins':
						resp = await websocket.recv()
						#While the station doesn't complete the charging or the car isn't unplugged, charging data process continues
						while resp!='Complete' and quit==False:
							print(f"> {resp} kWh consumed")
							await websocket.send(f"Received")
							battery += int(resp)
							resp = await websocket.recv()
						step += 1
				#Receiving of the bill and payment
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
				#Inform the customer to unplug
				elif step==5:
					print(f"--------------------------------------------")
					print("Unplug required")
					print(f"--------------------------------------------")
					step += 1
				#Quit the program
				elif step==-1:
					exit(0)
			else:
				#If the customer unplugged before the end of the process
				if step!=6:
					await websocket.send("Stop")
					print('Stopping...')
					#get the last amount of power
					print(f"> {resp} kWh consumed")
					await websocket.send(f"Received")
					battery += int(resp)
					resp = await websocket.recv()
					print(f"--------------------------------------------")
					print(f"> Charging stopped")
					await websocket.send("Stop transaction")
					#Waits for the bill and pays for it
					bill = await websocket.recv()
					print(f"> {bill} $ to pay")
					money -= float(bill)
					await websocket.send("Payed")
					print(f"> Payed")
					print("Balance :"+str(money)+" $")
				#If the process is finished, casually unplug
				else:
					await websocket.send("Unplugged")
				step=-1
				print('> Unplugged')

#Catches the SIGINT signals
signal.signal(signal.SIGINT, signal_handler)
#Runs the plug function
asyncio.get_event_loop().run_until_complete(plug())