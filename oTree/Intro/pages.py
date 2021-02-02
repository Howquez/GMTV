from otree.api import Currency as c, currency_range
from ._builtin import Page, WaitPage
from .models import Constants


class Intro_Welcome(Page):
    pass

class Intro_Instructions(Page):
    def js_vars(self):
        return dict(
            template="instructions",
        )

page_sequence = [Intro_Welcome, Intro_Instructions]
