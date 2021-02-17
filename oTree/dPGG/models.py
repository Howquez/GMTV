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
import random
import time

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
    rate_of_return = (efficiency_factor - 1)*100

    safe_rounds = 2 # number of rounds without any risk
    risk = 0.33 # risk of damage per round
    timeout = 10 # minutes
    patience = 6 # minutes



class Subsession(BaseSubsession):
    def creating_session(self):
        if self.round_number == 1:
            for p in self.get_players():
                p.participant.vars["endowments"] = []
                p.participant.vars["stock"] = []
                p.participant.vars["is_dropout"] = False
                p.participant.vars["is_residual_player"] = False
                if not "wait_page_arrival" in p.participant.vars:
                    p.participant.vars["wait_page_arrival"] = time.time()

    def group_by_arrival_time_method(self, waiting_players):
        if len(waiting_players) >= Constants.players_per_group:
            return waiting_players[:Constants.players_per_group]
        for player in waiting_players:
            if player.waiting_too_long():
                player.participant.vars["is_residual_player"] = True
                # make a single-player group.
                return [player]



class Group(BaseGroup):

    disaster = models.BooleanField(initial=False, doc="if true, negative effects on MPCR or stock will occur.")
    total_contribution = models.IntegerField(doc="sum of contributions in this round")
    average_contribution = models.FloatField(doc="average contribution in this round")
    individual_share = models.FloatField(doc="individual share each player receives from this round's contributions")
    bot_active = models.BooleanField(doc="denotes whether player in group dropped out such that a bot takes over", initial = False)

    def set_payoffs(self):

        if self.round_number > Constants.safe_rounds:
            if Constants.risk > random.uniform(0, 1):
                self.disaster = True

        if len(self.get_players()) == Constants.players_per_group:
            self.total_contribution = sum([p.contribution for p in self.get_players()])
            self.average_contribution = round(self.total_contribution / Constants.players_per_group, 2)
            self.individual_share = self.total_contribution * Constants.efficiency_factor / Constants.players_per_group

        for p in self.get_players():
            # players who were stuck on the initial wait page due to group member's drop outs have 0-earnings as well as
            # little bonus implemented as a payoff in the last round
            if p.participant.vars["is_residual_player"]:
                p.stock = 0
                p.gain = 0
                p.payoff = 0
                # give them a 2 Euro bonus
                if self.round_number == self.session.config["num_rounds"]:
                    p.payoff = c(Constants.initial_endowment)
            # all the others essentially earn their gains (which can be negative)
            else:
                p.gain = int(math.ceil(self.individual_share - p.contribution))

                # implement basic disaster damage
                if self.disaster:
                    p.gain = p.gain - 10

                # limited liability
                if p.gain < - p.endowment:
                    p.gain = - p.endowment

                p.stock = p.endowment + p.gain

                p.participant.vars["stock"].append(round(p.stock*self.session.config["real_world_currency_per_point"], 1))

                # payoff
                if p.round_number == 1:
                    p.payoff = c(p.stock)
                else:
                    p.payoff = c(p.gain)

                # Make sure participants do not earn anything if they drop out in four steps:
                #1: if they are marked as a dropout, they shouldn't earn anything
                if p.is_dropout:
                    if self.round_number < self.session.config["num_rounds"]:
                        p.payoff = c(0)
                #2: in their last round, also substract the participationn fee
                    else:
                        p.payoff = c(- self.session.config["participation_fee"]/self.session.config["real_world_currency_per_point"])
                #3: substract all the money they earned prior to dropping out
                if self.round_number > 1:
                    if not p.is_dropout == p.in_round(self.round_number - 1).is_dropout:
                        p.payoff = -p.endowment




class Player(BasePlayer):

    review_instructions = models.IntegerField(doc="Counts the number of times a player reviews instructions.")

    endowment = models.IntegerField(doc="the player's endowment in this round (equals her stock of last round)")
    contribution = models.IntegerField(min=0, doc="the player's contribution in this round")
    gain = models.CurrencyField(doc="each round's payoff as the difference of the individual_share and the player's contribution")
    stock = models.CurrencyField(doc="accumulated earnings of played rounds")
    is_dropout = models.BooleanField(doc="denotes whether player dropped out", initial = False)

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

    def waiting_too_long(self):
        return time.time() - self.participant.vars['wait_page_arrival'] > Constants.patience * 60
