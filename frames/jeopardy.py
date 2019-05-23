from asciimatics.widgets import Layout, Widget, Label, Divider, Button
from asciimatics.exceptions import NextScene, StopApplication
from frames.clue import ClueFrame, clue_position
from frames.parent_frame import ParentFrame
from asciimatics.event import KeyboardEvent
from asciimatics.screen import Screen
from CategoriesModel import categories

class JeopardyFrame(ParentFrame):
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

    def _clicked(self, screen, button):
        clue_position['column'] = button._location["x"]
        clue_position['row'] = button._location["y"]
        self.hide_button(clue_position['column'], clue_position['row'])
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
                button._name = f"{category_index},{clue_index}"
                button._location = {"x": category_index, "y": clue_index}
                button._on_click = lambda bound_value = button: self._clicked(screen, bound_value)

                self.layouts[clue_index + 1].add_widget(
                    button,
                    category_index
                )

                self.layouts[clue_index + 1].add_widget(Divider(draw_line=False, height=screen.height // 7), category_index)
