import asyncio
import readchar
import websockets
import socket
import json
import sys

name = ""

def update_name(user):
    global name
    name = user

async def buzz():
    async with websockets.connect('ws://localhost:8766') as websocket:
        data = {"event": "buzz", "name": name}
        await websocket.send(json.dumps(data))
        response = await websocket.recv()
        print(response)

async def hello():
    async with websockets.connect('ws://localhost:8766') as websocket:
        update_name(input("What's your name? "))
        data = {"event": "join", "name": name, "hostname": socket.gethostname()}
        await websocket.send(json.dumps(data))
        response = await websocket.recv()
        print(response)

asyncio.get_event_loop().run_until_complete(hello())

while True:
    key = ord(readchar.readkey())
    if key in (3, 4, 113):
        sys.exit()
    if key == 32:
        asyncio.run(buzz())
