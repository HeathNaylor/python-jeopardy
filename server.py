import json
import asyncio
import websockets
import websockets
from frames.player import buzzed_players, players
from storage.redis import Clue

ip = "localhost" 

def server():
    asyncio.set_event_loop(asyncio.new_event_loop())
    start_server = websockets.serve(hello, ip, 8766)

    asyncio.get_event_loop().run_until_complete(start_server)
    asyncio.get_event_loop().run_forever()

def join_player(event):
    for index, player in enumerate(players):
        if not player["hostname"] == event["hostname"]:
            continue
        players[index]["name"] = event["name"]
        return

    players.append({"hostname": event["hostname"], "name": event["name"], "points": 0})

def buzz_player_in(event):
    if not Clue.allowed_to_buzz():
        return False
    if event['name'] not in buzzed_players:
        buzzed_players.append(event['name'])
    return True

async def hello(websocket, path):
    event = await websocket.recv()
    event = json.loads(event)

    if event["event"] == 'join':
        join_player(event)
        await websocket.send(f"Welcome to Pythonic Jeopardy {event['name']}!")
    if event["event"] == 'buzz':
        if buzz_player_in(event):
            await websocket.send(f"{event['name']}, you hit the buzzer!")
            return
        await websocket.send(f"{event['name']}, you can not buzz in yet!")
