from asciimatics.widgets import Layout, Widget, Label, Divider
from asciimatics.exceptions import NextScene, StopApplication
from frames.parent_frame import ParentFrame
from asciimatics.event import KeyboardEvent
from asciimatics.screen import Screen

players = []
buzzed_players = []
allowed_to_buzz = False

class PlayersFrame(ParentFrame):
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
        layout2 = Layout([1,1])
        self.add_layout(layout)
        self.add_layout(layout2)

        padding = Label("", align='^', height=10)
        padding.custom_colour = "field"
        layout.add_widget(padding, 0)

        self.add_effect(self._figlet(self._canvas, {"text": "PLAYERS", "font": 'starwars'},[screen.width // 2, 1], 38))
        self.players_title = Label("Scores", height=2, align='^')
        self.players_label = Label("", height=1000, align='^')
        self.players_label.custom_colour = "field"
        layout2.add_widget(self.players_title, 0)
        layout2.add_widget(self.players_label, 0)

        self.buzzed_players_title = Label("Buzzed In", height=2, align='^')
        self.buzzed_players_label = Label("Test", height=10, align='^')
        self.buzzed_players_label.custom_colour = "field"
        layout2.add_widget(self.buzzed_players_title, 1)
        layout2.add_widget(self.buzzed_players_label, 1)
        self.fix()

    def _loaded(self):
        self.buzzed_players_label.text = "\n".join(buzzed_players)
        self.players_label.text = "\n".join([f"{player['name']} - {player['points']}" for player in players])

    def process_event(self, event):
        # Do the key handling for this Frame.
        if isinstance(event, KeyboardEvent):
            if event.key_code in [ord('p'), ord('P')]:
                raise NextScene("Players")
            if event.key_code in [ord('c'), ord('C')]:
                self.buzzed_players_label.text = ""
                buzzed_players.clear()
                raise NextScene("Players")
            if event.key_code in [ord('q'), ord('Q'), Screen.ctrl("c")]:
                raise NextScene("Main")
