from asciimatics.widgets import Layout, Widget, Label, Divider, Button
from asciimatics.exceptions import NextScene, StopApplication
from asciimatics.event import KeyboardEvent
from CategoriesModel import categories, Categories
from asciimatics.screen import Screen
from frames.player import players, buzzed_players
from frames.parent_frame import ParentFrame
from storage.redis import Clue, Player, Points

clue_position = {"row": 0, "column": 0}

class ClueFrame(ParentFrame):
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

        answer_padding = Label("", align='^', height=10)
        layout2.add_widget(question_padding, 0)

        self.buzzed_players = Label("", align='^')
        self.buzzed_players.custom_colour = "field"
        layout2.add_widget(self.buzzed_players, 0)

        # Prepare the Frame for use.
        self.fix()
 
    def _toggle_answer(self):
        if len(self.question.text):
            self.question.text = ""
            return

        self.question.text = Categories.getClueField(
            clue_position['column'],
            clue_position['row'],
            'question'
        )

    def _loaded(self):
        self.clue.text = Categories.getClueField(
            clue_position['column'],
            clue_position['row'],
            'clue'
        )

        self.buzzed_players.text = ", ".join(Player.all_buzzed_players_names())

    def add_points(self):
        buzzed_players = Player.all_buzzed_players()
        if not len(buzzed_players):
            return

        for index, player in enumerate(buzzed_players):
            if player == Player.get_first_buzzed_player():
                points = int(Categories.getClueField(
                    clue_position['column'],
                    clue_position['row'],
                    'points'
                ))

                Points.adjust_points(player, points)

    def remove_points(self):
        buzzed_players = Player.all_buzzed_players()
        if not len(buzzed_players):
            return

        for index, player in enumerate(buzzed_players):
            if player == Player.get_first_buzzed_player():
                points = int(Categories.getClueField(
                    clue_position['column'],
                    clue_position['row'],
                    'points'
                ))

                Points.adjust_points(player, (points * -1))

    def process_event(self, event):
        # Do the key handling for this Frame.
        if isinstance(event, KeyboardEvent):
            if event.key_code in [ord('r'), ord('R')]:
                self._toggle_answer()
            if event.key_code in [ord('b'), ord('B')]:
                Clue.allow_buzzer()
            if event.key_code in [ord('y'), ord('Y')]:
                self.add_points()
                Player.clear_buzzed_players()
                Clue.disallow_buzzer()
                raise NextScene("Main")
            if event.key_code in [ord('n'), ord('N')]:
                self.remove_points()
                Player.clear_buzzed_players()
                Clue.disallow_buzzer()
                raise NextScene("Main")
            if event.key_code in [ord('p'), ord('P')]:
                raise NextScene("Clue")
            if event.key_code in [ord('q'), ord('Q'), Screen.ctrl("c")]:
                self.clue.text = ""
                self.question.text = ""
                raise NextScene("Main")

        # Now pass on to lower levels for normal handling of the event.
        return super(ClueFrame, self).process_event(event)
