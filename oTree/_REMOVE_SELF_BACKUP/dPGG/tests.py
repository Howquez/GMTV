from otree.api import Currency as c, currency_range
from . import pages
from ._builtin import Bot
from otree.api import Submission
from .models import Constants
import random


class PlayerBot(Bot):
    def play_round(self):
        if self.round_number <= self.session.config["num_rounds"]:
            if self.round_number == Constants.belief_elicitation_round:
                if self.session.config["belief_elicitation"]:
                    yield pages.dPGG_Belief, dict(belief=random.randint(int(self.player.endowment/2),
                                                                        self.player.endowment)*Constants.num_others_per_group
                                                  )
            yield Submission(pages.dPGG_Decision, # in Gächter et al, subjects first contribute around 60%, then 30%
                             dict(contribution=int(self.player.endowment/2)),
                             # dict(contribution=int((100 - 6 * self.round_number)/100 * random.randint(int(self.player.endowment/5*2.5), #HI==2.5,LO==2
                             #                                                                           int(self.player.endowment/5*5))  #HI==5,  LO==3.5
                             #                       )
                             #      ),
                             check_html=False)
            if self.round_number == self.session.config["num_rounds"]:
                yield pages.dPGG_Results
                if random.randint(0, 100) > 90:
                    a = 0
                else:
                    a = random.randint(1, 3)
                yield pages.dPGG_Comprehension, dict(comprehension=a)
                yield pages.dPGG_Donation, dict(donation=random.randint(0, int(self.player.endowment/2)))