import asyncio
import readchar 
import websockets
import sys

name = "a"

async def buzz():
    print(name)

async def hello():
    name = await websocket.recv()
    print(f"< {name}")

    greeting = f"Hello {name}!"

    await websocket.send(greeting)
    print(f"> {greeting}")

start_server = websockets.serve(hello, 'localhost', 8766)
asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()

while True:
    key = ord(readchar.readkey())
    if key == 113:
        sys.exit()
    if key == 32:
        asyncio.run(buzz())
