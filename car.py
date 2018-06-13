#!/usr/bin/env python

import asyncio
import websockets
import time
import signal

"""
This program simulates the communication on the side of the car:
- launching this simulates the plugging
- sending SIGINT signal during the program simulates the unplugging/asks for the unplugging
"""

batteryCapacity = 500
quit = False
battery = 123
money = 500.0


# Handler for the SIGINT signal
def signal_handler(signal, frame):
    global quit
    quit = True


# Starts the connection
async def plug():
    async with websockets.connect('ws://localhost:8765') as websocket:
        await websocket.send(f"Plugged")
        print(f"> Plugged")
        resp = await websocket.recv()
        print(f"< {resp}")
        if resp == 'Connected':
            await sendCredentials(websocket)
        else:
            print("> Unable to connect")
            await endTransaction(websocket)


# Sends credentials to the station
async def sendCredentials(websocket):
    # Warn the station that the credentials will be sent
    await websocket.send(f"ID")
    # Waits for the user to enter an ID
    id = input("Enter your ID: ")
    await websocket.send(f"{id}")
    print(f"> ID sent")
    resp = await websocket.recv()
    print(f"--------------------------------------------")
    print(f"< {resp}")
    if resp == 'Authorized':
        await sendNeeds(websocket)
    else:
        await endTransaction(websocket)


# Sends informations to calculate amount of power to provide
async def sendNeeds(websocket):
    global battery
    global money
    # Amount of power needed
    needed = batteryCapacity - battery
    await websocket.send("Needs")
    await websocket.send(f"{needed}")
    print("> Charging request sent")
    # Amount of money that can be provided
    await websocket.send(f"{money}")
    print("> Money balance sent")
    # Waits for the amount of power allowed by the station
    resp = await websocket.recv()
    print(f"< {resp} kWh allowed")
    await websocket.send("Start")
    resp = await websocket.recv()
    print(f"> Starting the charge")
    print(f"--------------------------------------------")
    print(f"< {resp}")
    if resp == 'Charging begins':
        await chargingProcess(websocket)
    else:
        print("> Charging can't start")
        await stopTransaction(websocket)


async def chargingProcess(websocket):
    global battery
    resp = await websocket.recv()
    # While the station doesn't complete the charging or the car isn't unplugged, charging data process continues
    while resp != 'Complete' and quit == False:
        print(f"> {resp} kWh consumed")
        await websocket.send("Received")
        battery += int(resp)
        resp = await websocket.recv()
    if quit == True:
        await stopTransaction(websocket)
    else:
        await payment(websocket)


async def payment(websocket):
    global money
    bill = await websocket.recv()
    print(f"> {bill} $ to pay")
    money -= float(bill)
    await websocket.send("Payed")
    print(f"> Payed")
    print("Balance :" + str(money) + " $")
    resp = await websocket.recv()
    print(f"> {resp}")
    if quit == False:
        await endTransaction(websocket)
    else:
        await unplug(websocket)


async def stopTransaction(websocket):
    await websocket.send("Non received")
    print('Stopping...')
    resp = await websocket.recv()
    print(f"--------------------------------------------")
    print(f"> Charging stopped")
    # await websocket.send("Stop transaction")
    await payment(websocket)

async def endTransaction(websocket):
    await websocket.send("Ended")
    print(f"--------------------------------------------")
    print("Unplug required")
    print(f"--------------------------------------------")
    # Waits for the user to unplug the car
    await websocket.recv()
    # while quit == False:
    #     time.sleep(1)
    await unplug(websocket)


async def unplug(websocket):
    await websocket.send("Unplugged")
    print('> Unplugged')
    exit(0)


# Catches the SIGINT signals
signal.signal(signal.SIGINT, signal_handler)
# Runs the plug function
asyncio.get_event_loop().run_until_complete(plug())
