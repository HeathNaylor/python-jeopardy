from asciimatics.widgets import Frame, Layout, Widget, Label, Divider
from asciimatics.exceptions import NextScene, StopApplication
from asciimatics.event import KeyboardEvent
from asciimatics.screen import Screen

players = []

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
