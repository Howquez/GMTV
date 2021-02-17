from otree.api import Currency as c, currency_range
from ._builtin import Page, WaitPage
from .models import Constants
import time


class Intro_Welcome(Page):
    pass

class Intro_Instructions(Page):
    form_model = "player"
    form_fields = ["window_width", "window_height", "browser",
                   "CQ1_1", "CQ1_2", "CQ2_1", "CQ2_2",
                   "MCQ_1", "MCQ_2"]

    def js_vars(self):
        return dict(
            template="instructions",
        )


    def before_next_page(self):
        self.participant.vars['wait_page_arrival'] = time.time()
        print(self.participant.vars['wait_page_arrival'])

page_sequence = [Intro_Welcome, Intro_Instructions]
