from asciimatics.event import KeyboardEvent
from asciimatics.widgets import Frame, Layout, FileBrowser, Widget, Label, PopUpDialog, Text, Divider, Button
from asciimatics.scene import Scene
from asciimatics.screen import Screen
from asciimatics.exceptions import ResizeScreenError, NextScene, StopApplication
import sys
import os
from time import sleep
from asciimatics.effects import Cycle, Stars
from asciimatics.renderers import FigletText

categories = [
    Label("Data Types", align='^'),
    Label("Debugging", align='^'),
    Label("Modules, Functions", align='^'),
    Label("Selection", align='^'),
    Label("Iteration", align='^'),
    Label("Classes", align='^'),
]

values = [
    200,
    400,
    600,
    800,
    1000,
]

class DemoFrame(Frame):
    def __init__(self, screen):
        super(DemoFrame, self).__init__(
            screen,
            screen.height,
            screen.width,
            has_border=False,
            hover_focus=True,
            name="Pythonic Jeopardy!"
        )

        # Here we specify the amount of columns we want for Jeopardy
        jeopardy_columns = 6

        # We use list comprehension here to create a dynamicly sized list based on how many columns we specify above
        layout = Layout([100/jeopardy_columns for index in range(jeopardy_columns)], fill_frame=True)
        self.add_layout(layout)

        # Create the grid of categories and values
        for index in range(len(categories)):
            categories[index].custom_colour = "field"
            layout.add_widget(categories[index], index)
            layout.add_widget(Divider(), index)

            for value_index in range(len(values)):
                layout.add_widget(Button(values[value_index], self._clicked), index)

        # Prepare the Frame for use.
        self.fix()

    def _clicked(self):
        raise NextScene("Main")

    def process_event(self, event):
        # Do the key handling for this Frame.
        if isinstance(event, KeyboardEvent):
            if event.key_code in [ord('q'), ord('Q'), Screen.ctrl("c")]:
                raise StopApplication("User quit")

        # Now pass on to lower levels for normal handling of the event.
        return super(DemoFrame, self).process_event(event)

def demo(screen, old_scene):
    screen.play([Scene([DemoFrame(screen)], name="Main")], stop_on_resize=True, start_scene=old_scene, allow_int=True)

last_scene = None
while True:
    try:
        Screen.wrapper(demo, catch_interrupt=False, arguments=[last_scene])
        sys.exit(0)
    except ResizeScreenError as e:
        last_scene = e.scene
