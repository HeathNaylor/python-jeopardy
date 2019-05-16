from asciimatics.widgets import Frame, Layout, FileBrowser, Widget, Label, PopUpDialog, Text, Divider, Button
from asciimatics.exceptions import ResizeScreenError, NextScene, StopApplication
from asciimatics.renderers import SpeechBubble, FigletText, Box
from asciimatics.effects import Cycle, Stars, Print, Clock
from asciimatics.event import KeyboardEvent
from asciimatics.screen import Screen
from asciimatics.scene import Scene
import sys
import os

categories = [
    "Data Types",
    "Debugging",
    "Modules, Functions",
    "Selection",
    "Iteration",
    "Classes",
]

values = [
    200,
    400,
    600,
    800,
    1000,
]

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
        layout = Layout([100/jeopardy_columns for index in range(jeopardy_columns)], fill_frame=True)
        self.add_layout(layout)
        self.define_grid(layout)

        # Prepare the Frame for use.
        self.fix()

    def _clicked(self):
        raise NextScene("Clue")

    def process_event(self, event):
        # Do the key handling for this Frame.
        if isinstance(event, KeyboardEvent):
            if event.key_code in [ord('q'), ord('Q'), Screen.ctrl("c")]:
                raise StopApplication("User quit")

        # Now pass on to lower levels for normal handling of the event.
        return super(JeopardyFrame, self).process_event(event)

    def define_grid(self, layout):
        # Create the grid of categories and values
        for index in range(len(categories)):
            category = Label(categories[index], align='^')
            category.custom_colour = "field"
            layout.add_widget(category, index)
            layout.add_widget(Divider(), index)

            for value_index in range(len(values)):
                layout.add_widget(Button(values[value_index], self._clicked), index)
                layout.add_widget(Divider(draw_line=False, height=6), index)

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
        layout = Layout([1], fill_frame=True)
        self.add_layout(layout)
        self.add_effect(self._speak(self._canvas, {"text": "CLUE", "font": 'starwars'},[screen.width // 2, 1], 20))
        category = Label("These data types are all examples of Sequence types or ordered sets.", align='^')
        category.custom_colour = "field"
        layout.add_widget(category, 0)

        # Prepare the Frame for use.
        self.fix()
 
    def _speak(self, screen, text, pos, offset):
        return Print(
            screen,
            FigletText(text["text"], text["font"]),
            x=pos[0] - offset, y=pos[1],
            colour=Screen.COLOUR_WHITE,
            clear=False,
            bg=Screen.COLOUR_BLUE
        )

    def process_event(self, event):
        # Do the key handling for this Frame.
        if isinstance(event, KeyboardEvent):
            if event.key_code in [ord('q'), ord('Q'), Screen.ctrl("c")]:
                raise NextScene("Main")

        # Now pass on to lower levels for normal handling of the event.
        return super(ClueFrame, self).process_event(event)


def jeopardy(screen, old_scene):
    scenes = [
        Scene([JeopardyFrame(screen)], name="Main"),
        Scene([ClueFrame(screen)], name="Clue")
    ]
    screen.play(scenes, stop_on_resize=True, start_scene=old_scene, allow_int=True)

last_scene = None
while True:
    try:
        Screen.wrapper(jeopardy, catch_interrupt=True, arguments=[last_scene])
        sys.exit(0)
    except ResizeScreenError as e:
        last_scene = e.scene
