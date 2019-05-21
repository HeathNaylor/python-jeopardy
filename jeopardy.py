from asciimatics.widgets import Frame, Layout, FileBrowser, Widget, Label, PopUpDialog, Text, Divider, Button, PopupMenu
from asciimatics.exceptions import ResizeScreenError, NextScene, StopApplication
from asciimatics.renderers import SpeechBubble, FigletText, Box
from asciimatics.effects import Cycle, Stars, Print, Clock
from asciimatics.event import KeyboardEvent
from asciimatics.screen import Screen
from asciimatics.scene import Scene
from CategoriesModel import categories
import threading
import asyncio
import websockets
import sys
import os

clue_position = {"row": 0, "column": 0}
players = []

class JeopardyFrame(Frame):
    def __init__(self, screen):
        super(JeopardyFrame, self).__init__(
            screen,
            screen.height,
            screen.width,
            has_border=False,
            hover_focus=True,
            name="Pythonic Jeopardy!"
        )

        # We use list comprehension here to create a dynamicly sized list based on how many columns we specify above
        jeopardy_columns = 6
        jeopardy_rows = 6
        self.layouts = [Layout([100/jeopardy_columns for index in range(jeopardy_columns)]) for index in range(jeopardy_rows)]
        [self.add_layout(layout) for layout in self.layouts]
        self.define_grid(screen)

        # Prepare the Frame for use.
        self.fix()

    def _clicked(self, screen, button_location):
        clue_position['column'] = button_location["x"]
        clue_position['row'] = button_location["y"]
        raise NextScene("Clue")

    def process_event(self, event):
        # Do the key handling for this Frame.
        if isinstance(event, KeyboardEvent):
            if event.key_code in [ord('q'), ord('Q'), Screen.ctrl("c")]:
                raise StopApplication("User quit")
            if event.key_code in [ord('p'), ord('P')]:
                raise NextScene("Players")

        # Now pass on to lower levels for normal handling of the event.
        return super(JeopardyFrame, self).process_event(event)

    def define_grid(self, screen):
        # Create the grid of categories and values
        for category_index in range(len(categories)):
            category = Label(categories[category_index]['category'], align='^')
            category.custom_colour = "field"
            self.layouts[0].add_widget(category, category_index)
            self.layouts[0].add_widget(Divider(), category_index)

            for clue_index in range(len(categories[category_index]['clues'])):
                button = Button(
                    categories[category_index]["clues"][clue_index]["points"],
                    self._clicked
                )
                button._location = {"x": category_index, "y": clue_index}
                button._on_click = lambda bound_value = button._location: self._clicked(screen, bound_value)

                self.layouts[clue_index + 1].add_widget(
                    button,
                    category_index
                )

                self.layouts[clue_index + 1].add_widget(Divider(draw_line=False, height=screen.height // 7), category_index)

class ClueFrame(Frame):
    def __init__(self, screen):
        super(ClueFrame, self).__init__(
            screen,
            screen.height,
            screen.width,
            has_border=False,
            hover_focus=True,
            name="Jeopardy Clue"
        )
        layout = Layout([1])
        layout2 = Layout([1])
        self.add_layout(layout)
        self.add_layout(layout2)
        self.add_effect(self._figlet(self._canvas, {"text": "CLUE", "font": 'starwars'},[screen.width // 2, 1], 20))

        padding = Label("", align='^', height=10)
        padding.custom_colour = "field"
        layout.add_widget(padding, 0)

        self.clue = Label("", align='^')
        self.clue.custom_colour = "field"
        layout2.add_widget(self.clue, 0)

        question_padding = Label("", align='^', height=5)
        layout2.add_widget(question_padding, 0)

        self.question = Label("", align='^')
        self.question.custom_colour = "field"
        layout2.add_widget(self.question, 0)

        # Prepare the Frame for use.
        self.fix()
 
    def _figlet(self, screen, text, pos, offset):
        return Print(
            screen,
            FigletText(text["text"], text["font"]),
            x=pos[0] - offset, y=pos[1],
            colour=Screen.COLOUR_WHITE,
            clear=False,
            bg=Screen.COLOUR_BLUE
        )

    def _toggle_answer(self):
        if len(self.question.text):
            self.question.text = ""
            return

        self.question.text = categories[clue_position['column']]['clues'][clue_position['row']]['question']

    def _loaded(self):
        self.clue.text = categories[clue_position['column']]['clues'][clue_position['row']]['clue']


    def process_event(self, event):
        # Do the key handling for this Frame.
        if isinstance(event, KeyboardEvent):
            if event.key_code == ord('r'):
                self._toggle_answer()
            if event.key_code in [ord('q'), ord('Q'), Screen.ctrl("c")]:
                self.clue.text = ""
                self.question.text = ""
                raise NextScene("Main")

        # Now pass on to lower levels for normal handling of the event.
        return super(ClueFrame, self).process_event(event)

class PlayersFrame(Frame):
    def __init__(self, screen):
        super(PlayersFrame, self).__init__(
            screen,
            screen.height,
            screen.width,
            has_border=False,
            hover_focus=True,
            name="Players"
        )
        layout = Layout([1])
        layout2 = Layout([1])
        self.add_layout(layout)
        self.add_layout(layout2)

        padding = Label("", align='^', height=5)
        padding.custom_colour = "field"
        layout.add_widget(padding, 0)

        self.players = Label("Test", height=10, align='^')
        self.players.custom_colour = "field"
        layout2.add_widget(self.players, 0)
        self.fix()

    def _loaded(self):
        self.players.text = "\n".join(players)

    def process_event(self, event):
        # Do the key handling for this Frame.
        if isinstance(event, KeyboardEvent):
            if event.key_code in [ord('p'), ord('P')]:
                raise NextScene("Players")
            if event.key_code in [ord('c'), ord('C')]:
                players.clear()
                raise NextScene("Players")
            if event.key_code in [ord('q'), ord('Q'), Screen.ctrl("c")]:
                raise NextScene("Main")

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

thread = threading.Thread(target=server)
thread.start()

last_scene = None
while True:
    try:
        Screen.wrapper(jeopardy, catch_interrupt=True, arguments=[last_scene])
        sys.exit(0)
    except ResizeScreenError as e:
        last_scene = e.scene
