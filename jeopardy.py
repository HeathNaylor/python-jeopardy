from asciimatics.widgets import Frame, Layout, FileBrowser, Widget, Label, PopUpDialog, Text, Divider, Button, PopupMenu
from asciimatics.exceptions import ResizeScreenError, NextScene, StopApplication
from asciimatics.renderers import SpeechBubble, FigletText, Box
from asciimatics.effects import Cycle, Stars, Print, Clock
from asciimatics.event import KeyboardEvent
from asciimatics.screen import Screen
from asciimatics.scene import Scene
from CategoriesModel import categories
import sys
import os

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
        layouts = [Layout([100/jeopardy_columns for index in range(jeopardy_columns)]) for index in range(jeopardy_rows)]
        [self.add_layout(layout) for layout in layouts]
        self.define_grid(layouts, screen.height)

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

    def define_grid(self, layouts, screen_height):
        # Create the grid of categories and values
        for index in range(len(categories)):
            category = Label(categories[index]['category'], align='^')
            category.custom_colour = "field"
            layouts[0].add_widget(category, index)
            layouts[0].add_widget(Divider(), index)

            for value_index in range(len(categories[index]['clues'])):
                layouts[value_index + 1].add_widget(Button(categories[index]["clues"][value_index]["points"], self._clicked), index)
                layouts[value_index + 1].add_widget(Divider(draw_line=False, height=screen_height // 7), index)

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
        self.padding = Label("", align='^', height=10)
        category = Label("These data types are all examples of Sequence types or ordered sets.", align='^', height=2)
        self.padding.custom_colour = "field"
        category.custom_colour = "field"
        layout.add_widget(self.padding, 0)
        layout2.add_widget(category, 0)

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
        if len(self.padding.text):
            self.padding.text = ""
            return

        self.padding.text = "Partayyy!"


    def process_event(self, event):
        # Do the key handling for this Frame.
        if isinstance(event, KeyboardEvent):
            if event.key_code == ord('r'):
                self._toggle_answer()
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
