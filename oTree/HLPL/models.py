from otree.api import (
    models,
    widgets,
    BaseConstants,
    BaseSubsession,
    BaseGroup,
    BasePlayer,
    Currency as c,
    currency_range,
)

import random

author = 'Your name here'

doc = """
Inspired by https://github.com/felixholzmeister/mpl
"""


class Constants(BaseConstants):
    name_in_url = 'HLPL'
    players_per_group = None
    num_rounds = 1
    num_choices = 11
    lottery_price = 100



class Subsession(BaseSubsession):
    def creating_session(self):
        n = Constants.num_choices
        for p in self.get_players():

            indices = [j for j in range(1, n + 1)]
            # indices.append(n)
            certainty_equivalents = [(k-1)*10 for k in indices]

            form_fields = ["choice_" + str(k) for k in indices]

            p.participant.vars["mpl_choices"] = list(
                zip(indices, form_fields, certainty_equivalents)
            )

            p.participant.vars["mpl_index_to_pay"] = random.choice(indices)
            p.participant.vars["mpl_choice_to_pay"] = "choice_" + str(p.participant.vars["mpl_index_to_pay"])

            p.participant.vars['mpl_choices_made'] = [None for j in range(1, n + 1)]


class Group(BaseGroup):
    pass


class Player(BasePlayer):


    review_instructions = models.IntegerField(doc="Counts the number of times a player reviews instructions.",
                                              initial=0,
                                              blank=True)
    review_contact = models.IntegerField(doc="Counts the number of times a player reviews contact information.",
                                         initial=0,
                                         blank=True)




    for j in range(1, Constants.num_choices + 1):
        locals()['choice_' + str(j)] = models.StringField()
    del j

    random_draw = models.IntegerField()
    choice_to_pay = models.StringField()
    option_to_pay = models.StringField()
    inconsistent = models.IntegerField()
    switching_row = models.IntegerField()

    def set_payoffs(self):
        self.random_draw = random.randint(0, 100)
        self.choice_to_pay = self.participant.vars["mpl_choice_to_pay"]
        self.option_to_pay = getattr(self, self.choice_to_pay)

        if self.option_to_pay == "lottery":
            if self.random_draw <= 50:
                self.payoff = Constants.lottery_price
            else:
                self.payoff = 0
        else:
            self.payoff = self.participant.vars["mpl_index_to_pay"]*10

        self.participant.vars["mpl_payoff"] = self.payoff



    def set_consistency(self):
        n = Constants.num_choices
        # replace "lottery"s by 1's and "certainty"s by 0's
        self.participant.vars["mpl_choices_made"] = [
            1 if j == "lottery" else 0 for j in self.participant.vars["mpl_choices_made"]
        ]

        # check for multiple switching behavior
        for j in range(1, n):
            choices = self.participant.vars["mpl_choices_made"]
            self.inconsistent = 1 if choices[j] > choices[j - 1] else 0
            if self.inconsistent == 1:
                break



    def set_switching_row(self):
        # set switching point to row number of first "certainty" choice
        if self.inconsistent == 0:
            self.switching_row = sum(self.participant.vars["mpl_choices_made"]) + 1
