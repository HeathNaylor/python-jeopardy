import json
import asyncio
import websockets
import websockets
from frames.player import buzzed_players, players

def server():
    asyncio.set_event_loop(asyncio.new_event_loop())
    start_server = websockets.serve(hello, '192.168.1.232', 8766)

    asyncio.get_event_loop().run_until_complete(start_server)
    asyncio.get_event_loop().run_forever()

def join_player(event):
    for index, player in enumerate(players):
        if not player["hostname"] == event["hostname"]:
            continue
        players[index]["name"] = event["name"]
        return

    players.append({"hostname": event["hostname"], "name": event["name"], "points": 0})

async def hello(websocket, path):
    event = await websocket.recv()
    event = json.loads(event)

    if event["event"] == 'join':
        join_player(event)
        await websocket.send(f"Welcome to Pythonic Jeopardy {event['name']}!")
    if event["event"] == 'buzz':
        buzzed_players.append(event['name'])
        greeting = f"{event['name']}, you hit the buzzer!"
        await websocket.send(greeting)
