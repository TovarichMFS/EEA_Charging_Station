#!/usr/bin/env python

# WS server example

import asyncio
import websockets

async def handle(websocket, path):
    call = await websocket.recv()
    print(f"< {call}")

    resp = f"Connected"

    await websocket.send(resp)
    print(f"> {resp}")

    call = await websocket.recv()
    if call!='':
	    resp = f"Authorized"
	    await websocket.send(resp)
	    print(f"> {resp}")

start_server = websockets.serve(handle, 'localhost', 8765)

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()