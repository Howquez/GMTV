from otree.api import Currency as c, currency_range
from . import pages
from ._builtin import Bot
from otree.api import Submission

from .models import Constants


class PlayerBot(Bot):
    def play_round(self):
        yield pages.Intro_Welcome
        yield pages.Intro_Instructions, dict(window_width=1, window_height=1, browser="Chrome Canary",
                                             CQ1_1=20, CQ1_2=20, CQ2_1=25, CQ2_2=25,
                                             MCQ_1=['2', '3'], MCQ_2=['2', '3'])
