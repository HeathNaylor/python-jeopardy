import asyncio
import websockets
import websockets
from frames.player import players

def server():
    asyncio.set_event_loop(asyncio.new_event_loop())
    start_server = websockets.serve(hello, 'localhost', 8765)

    asyncio.get_event_loop().run_until_complete(start_server)
    asyncio.get_event_loop().run_forever()

async def hello(websocket, path):
    name = await websocket.recv()
    players.append(name)
    greeting = f"Hello {name}!"
    await websocket.send(greeting)
