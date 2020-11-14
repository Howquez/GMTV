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

import math

author = "Hauke Roggenkamp"

doc = """
Dynamic Public Goods Game where the current round's earnings determine the next round's endowment
"""


class Constants(BaseConstants):
    name_in_url = 'dPGG'
    players_per_group = 3
    num_others_per_group = players_per_group - 1
    max_rounds = 15 # set maximum number of rounds possible
    num_rounds = max_rounds
    initial_endowment = 20
    efficiency_factor = 1.25 # (MPCR) Marginal Per Capita Return per round


class Subsession(BaseSubsession):
    def creating_session(self):
        if self.round_number == 1:
            for p in self.get_players():
                p.participant.vars["endowments"] = []
                p.participant.vars["stock"] = []


class Group(BaseGroup):

    total_contribution = models.IntegerField(doc="sum of contributions in this round")
    average_contribution = models.FloatField(doc="average contribution in this round")
    individual_share = models.FloatField(doc="individual share each player receives from this round's contributions")

    def set_payoffs(self):

        self.total_contribution = sum([p.contribution for p in self.get_players()])
        self.average_contribution = round(self.total_contribution / Constants.players_per_group, 2)
        self.individual_share = self.total_contribution * Constants.efficiency_factor / Constants.players_per_group

        for p in self.get_players():

            p.gain = int(math.ceil(self.individual_share - p.contribution))
            p.stock = p.endowment + p.gain

            # limited liability
            if p.stock < 0:
                p.stock = 0

            p.participant.vars["stock"].append(round(p.stock*self.session.config["real_world_currency_per_point"], 1))

            if self.round_number == 1:
                p.payoff = c(p.stock)
            else:
                p.payoff = c(p.gain)

class Player(BasePlayer):

    endowment = models.IntegerField(doc="the player's endowment in this round (equals her stock of last round)")
    contribution = models.IntegerField(min=0, doc="the player's contribution in this round")
    gain = models.IntegerField(doc="each round's payoff as the difference of the individual_share and the player's contribution")
    stock = models.CurrencyField(doc="accumulated earnings of played rounds")

    def start(self):
        if self.round_number == 1:
            self.endowment = Constants.initial_endowment
        else:
            self.endowment = int(self.in_round(self.round_number - 1).stock)
        self.participant.vars["endowments"].append(self.endowment)


    def contribution_max(self):
        if self.round_number == 1:
            return Constants.initial_endowment
        else:
            return self.in_round(self.round_number - 1).stock