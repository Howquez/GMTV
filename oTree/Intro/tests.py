from otree.api import Currency as c, currency_range
from . import pages
from ._builtin import Bot
from otree.api import Submission

from .models import Constants


class PlayerBot(Bot):
    def play_round(self):
        yield pages.Intro_Welcome
        yield Submission(pages.Intro_Instructions, #dict(contribution=random.randint(0, self.player.endowment)),
                         check_html=False)
