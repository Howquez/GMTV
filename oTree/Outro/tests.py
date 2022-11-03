from otree.api import Currency as c, currency_range
from . import *
from otree.api import Bot

import random

class PlayerBot(Bot):
    def play_round(self):
        yield Outro_Personality, dict(PQ01=random.randint(0, 6),
                                            PQ02=random.randint(0, 6),
                                            PQ03=random.randint(0, 6),
                                            PQ04=random.randint(0, 6),
                                            PQ05=random.randint(0, 6),
                                            PQ06=random.randint(0, 6),
                                            PQ07=random.randint(0, 6),
                                            PQ08=random.randint(0, 6),
                                            PQ09=random.randint(0, 6),
                                            PQ10=random.randint(0, 6),
                                            PQ11=random.randint(0, 6),
                                            PQ12=random.randint(0, 6),
                                            PQ13=random.randint(0, 6),
                                            PQ14=random.randint(0, 6))
        yield Outro_Covariates, dict(Age=random.randint(18, 66),
                                           Gender=random.choice(["diverse", "male", "female", "not specified"]),
                                           Education=random.randint(0, 8),
                                           Income=random.randint(0, 5))
        yield Outro_CLICCS, dict(CLICCS1="lorem ipsum 1", CLICCS2="lorem ipsum 2")

