from asciimatics.exceptions import ResizeScreenError
from asciimatics.screen import Screen
from asciimatics.scene import Scene
from frames.jeopardy import JeopardyFrame
from frames.player import PlayersFrame
from frames.clue import ClueFrame
import threading
import server
import sys
import os

def jeopardy(screen, old_scene):
    clue_frame = ClueFrame(screen)
    clue_frame._on_load = lambda: clue_frame._loaded()

    players_frame = PlayersFrame(screen)
    players_frame._on_load = lambda: players_frame._loaded()

    scenes = [
        Scene([JeopardyFrame(screen)], name="Main"),
        Scene([clue_frame], name="Clue", clear=True),
        Scene([players_frame], name="Players"),
    ]
    screen.play(scenes, stop_on_resize=True, start_scene=old_scene, allow_int=True)


thread = threading.Thread(target=server.server)
thread.start()

last_scene = None
while True:
    try:
        Screen.wrapper(jeopardy, catch_interrupt=True, arguments=[last_scene])
        sys.exit(0)
    except ResizeScreenError as e:
        last_scene = e.scene
