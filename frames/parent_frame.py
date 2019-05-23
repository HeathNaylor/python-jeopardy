from asciimatics.renderers import FigletText
from asciimatics.widgets import Frame
from asciimatics.effects import Print
from asciimatics.screen import Screen

class ParentFrame(Frame):
    def _figlet(self, screen, text, pos, offset):
        return Print(
            screen,
            FigletText(text["text"], text["font"]),
            x=pos[0] - offset, y=pos[1],
            colour=Screen.COLOUR_WHITE,
            clear=False,
            bg=Screen.COLOUR_BLUE
        )

    def hide_button(self, column, row):
        button = self.find_widget(f"{column},{row}")
        button._is_disabled = True

