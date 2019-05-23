from asciimatics.widgets import Layout, Label
from asciimatics.exceptions import NextScene
from asciimatics.event import KeyboardEvent
from asciimatics.screen import Screen
from frames.parent_frame import ParentFrame

class EntryFrame(ParentFrame):
    def __init__(self,screen):
        super(EntryFrame, self).__init__(
                screen,
                screen.height,
                screen.width,
                has_border=False,
                hover_focus=True,
                name="Pythonic Jeopardy!"
            )

        layout = Layout([1])
        self.add_layout(layout)

        self.add_effect(self._figlet(self._canvas, {"text": "PYTHONIC", "font": 'starwars'},[screen.width // 2, 5], 40))
        self.add_effect(self._figlet(self._canvas, {"text": "JEOPARDY", "font": 'starwars'},[screen.width // 2, 15], 42))

    def process_event(self, event):
        # Do the key handling for this Frame.
        if isinstance(event, KeyboardEvent):
            raise NextScene("Main")
