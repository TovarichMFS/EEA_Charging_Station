#!/usr/bin/env python

import asyncio
import websockets

id = "ouiouoiuioui"

async def plug():
    async with websockets.connect('ws://localhost:8765') as websocket:

        await websocket.send('pluged')
        print(f"> pluged")

        resp = await websocket.recv()
        print(f"< {resp}")
        if resp=='Connected':
        	await websocket.send(f"> {id}")
        	print(f"> ID sent")
        	resp = await websocket.recv()
        	print(f"< {resp}")

asyncio.get_event_loop().run_until_complete(plug())