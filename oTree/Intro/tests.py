from otree.api import Currency as c, currency_range
from . import pages
from ._builtin import Bot
from otree.api import Submission

from .models import Constants


class PlayerBot(Bot):
    def play_round(self):
        yield pages.Intro_Welcome
        yield pages.Intro_Instructions, dict(window_width=1, window_height=1, browser="Chrome Canary",
                                             CQ1_1=int(Constants.initial_endowment),
                                             CQ1_2=int(Constants.initial_endowment),
                                             CQ2_1=int(Constants.initial_endowment * Constants.efficiency_factor),
                                             CQ2_2=int(Constants.initial_endowment * Constants.efficiency_factor),
                                             #MCQ_1=['2', '3'], MCQ_2=['2', '3'],
                                             CQ3_1=int(30 + Constants.efficiency_factor * 40 / Constants.group_size),
                                             CQ3_2=int(30 - 16 + Constants.efficiency_factor * (40+16) / Constants.group_size))
