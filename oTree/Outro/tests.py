from otree.api import Currency as c, currency_range
from . import pages
from ._builtin import Bot
from .models import Constants
import random

class PlayerBot(Bot):
    def play_round(self):
        yield pages.Outro_Covariates, dict(Age=random.randint(18, 25), Gender="diverse", Education="uni",
                                                Income=random.randint(20000, 50000), Comprehension="yes")
        yield pages.Outro_CLICCS, dict(CLICCS1="lorem ipsum", CLICCS2="lorem ipsum")

