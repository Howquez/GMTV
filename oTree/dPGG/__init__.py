import math
import random
import time

from otree.api import *


author = "Hauke Roggenkamp"
doc = """
Dynamic Public Goods Game where the current round's earnings determine the next round's endowment
"""


class Constants(BaseConstants):
    name_in_url = "dPGG"
    players_per_group = 4  # adjust Constants.group_size in A_Intro App when adjusting this
    num_others_per_group = players_per_group - 1
    num_rounds = 10
    initial_endowment = 20
    efficiency_factor = 1.5  # /4 = (MPCR) Marginal Per Capita Return per round
    rate_of_return = (efficiency_factor - 1) * 100
    safe_rounds = 0  # number of rounds without any risk
    threshold = 0.5  # fraction of a group's endowment that has to be contributed such that no disaster can occur
    belief_elicitation_round = 1
    elicitation_bonus = 30  # points
    timeout = 4  # minutes
    patience = 10  # minutes
    patience_bonus = 20  # points


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    residual = models.BooleanField(initial=False, doc="if true, group is incomplete")
    EWE = models.BooleanField(initial=False, doc="if true, extreme weather event occurred")
    total_contribution = models.IntegerField(doc="sum of contributions in this round")
    average_contribution = models.FloatField(doc="average contribution in this round")
    individual_share = models.IntegerField(
        doc="individual share each player receives from this round's contributions"
    )
    bot_active = models.BooleanField(
        doc="denotes whether player in group dropped out such that a bot takes over", initial=False
    )
    wealth = models.IntegerField(doc="sum of endowments at the beginning of a round")


class Player(BasePlayer):
    comprehension = models.IntegerField(
        doc="Respondent's understanding of the tasks",
        label="Haben Sie die Aufgabe gut verstanden?",
        choices=[[0, "Nein"], [1, "Eher nicht"], [2, "Eher schon"], [3, "Ja"]],
        widget=widgets.RadioSelect,
    )
    donation = models.IntegerField(doc="Participant's donation (in points) for carbon offsetting")
    review_instructions = models.IntegerField(
        doc="Counts the number of times a player reviews instructions.", initial=0, blank=True
    )
    review_contact = models.IntegerField(
        doc="Counts the number of times a player reviews contact information.",
        initial=0,
        blank=True,
    )
    wait_time_left = models.IntegerField(
        doc="denotes the time a player has to wait for others to arrive on WaitPage"
    )
    endowment = models.IntegerField(
        doc="the player's endowment in this round (equals her stock of last round)"
    )
    contribution = models.IntegerField(min=0, doc="the player's contribution in this round")
    belief = models.IntegerField(
        min=0, doc="the player's belief about the other player's average contribution"
    )
    gross_gain = models.IntegerField(
        doc="each round's gross earnings as the difference of the individual_share and the player's contribution"
    )
    gain = models.IntegerField(
        doc="each round's net earnings as the difference between stock and endowment (incorporating possible damage)"
    )
    stock = models.IntegerField(doc="accumulated earnings of played rounds")
    is_dropout = models.BooleanField(doc="denotes whether player dropped out", initial=False)


# FUNCTIONS
def creating_session(subsession: Subsession):
    print("lets go")
    if subsession.round_number == 1:
        for p in subsession.get_players():
            p.participant.vars["belief_elicitation_round"] = Constants.belief_elicitation_round
            p.participant.vars["endowments"] = []
            p.participant.vars["stock"] = []
            p.participant.vars["euros"] = []
            p.participant.vars["is_dropout"] = False
            p.participant.vars["is_residual_player"] = False
            if not "wait_page_arrival" in p.participant.vars:
                p.participant.vars["wait_page_arrival"] = time.time()


def group_by_arrival_time_method(subsession: Subsession, waiting_players):
    if len(waiting_players) >= Constants.players_per_group:
        return waiting_players[: Constants.players_per_group]
    for player in waiting_players:
        player.wait_time_left = int(
            math.ceil(
                Constants.patience
                - (time.time() - player.participant.vars['wait_page_arrival']) / 60
            )
        )
        if waiting_too_long(player):
            player.participant.vars["is_residual_player"] = True
            player.group.residual = True
            # make a single-player group.
            return [player]


def set_group_variables(group: Group):
    if len(group.get_players()) == Constants.players_per_group:
        group.total_contribution = sum([p.contribution for p in group.get_players()])
        group.average_contribution = round(
            group.total_contribution / Constants.players_per_group, 2
        )
        group.individual_share = int(
            math.ceil(
                group.total_contribution * Constants.efficiency_factor / Constants.players_per_group
            )
        )
        group.wealth = sum([p.endowment for p in group.get_players()])
        # alternatively, define wealth as the last round's stock
        # self.wealth = sum([p.stock for p in self.in_round(self.round_number - 1).get_players()])


def set_disaster(group: Group):
    # random risk lottery
    if not group.residual:
        if group.round_number > Constants.safe_rounds:
            if group.session.config["risk"] > random.uniform(0, 1):
                group.EWE = True


def set_payoffs(group: Group):
    # call  methods
    set_group_variables(group)
    # calculate player-level-variables
    for p in group.get_players():
        # players who were stuck on the initial wait page due to group member's drop outs have 0-earnings plus a
        # little bonus implemented as a payoff in the last round
        if p.participant.vars["is_residual_player"]:
            p.stock = 0
            p.gain = 0
            p.payoff = 0
            # give them a patience bonus
            if group.round_number == group.session.config["num_rounds"]:
                p.payoff = c(Constants.patience_bonus)
        # all the others essentially earn their gains
        else:
            p.gross_gain = group.individual_share - p.contribution
            p.stock = p.endowment + p.gross_gain
            p.gain = (
                p.stock - p.endowment
            )  # this may differ from gross_gain if damages (due to EWE arise)
            # p.participant.vars["stock"].append(round(p.stock*self.session.config["real_world_currency_per_point"], 1))
            p.participant.vars["stock"].append(p.stock)
            p.participant.vars["euros"].append(c(p.stock).to_real_world_currency(group.session))
            if p.round_number == 1:
                p.payoff = c(p.stock)
            else:
                p.payoff = c(p.gain)
            # add payoff from belief elicitation
            if group.round_number == Constants.belief_elicitation_round:
                if group.session.config["belief_elicitation"]:
                    others_contribution = group.total_contribution - p.contribution
                    bonus = c(Constants.elicitation_bonus - abs(p.belief - others_contribution))
                    p.participant.vars["belief_bonus"] = bonus
                    p.participant.vars["belief_payoff"] = c(bonus).to_real_world_currency(
                        group.session
                    )
                else:
                    p.participant.vars["belief_bonus"] = 0
                # vars for Outro
                # p.participant.vars["guess"] = 0
                # p.participant.vars["others_contribution"] = others_contribution
                # p.participant.vars["belief"] = p.belief
                # p.participant.vars["belief_bonus"] = c(Constants.elicitation_bonus).to_real_world_currency(
                #     self.session)
                # actual payoff operation
                # .to_real_world_currency(self.session)
            # Make sure participants do not earn anything if they drop out in two steps:
            # 1: if they are marked as a dropout, they shouldn't earn anything
            if p.is_dropout:
                if group.round_number <= group.session.config["num_rounds"]:
                    p.payoff = 0
                    if group.round_number == 1:
                        p.payoff = -(
                            group.session.config["participation_fee"]
                            / group.session.config["real_world_currency_per_point"]
                        )
            # 2: substract their endowment, as well as the participation fee and the belief elicitation bonus
            # immediately after their dropout
            if group.round_number > 1:
                if not p.is_dropout == p.in_round(group.round_number - 1).is_dropout:
                    p.payoff = -(
                        p.endowment
                        + group.session.config["participation_fee"]
                        / group.session.config["real_world_currency_per_point"]
                    )
            # store payoff in participant var
            if group.round_number == group.session.config["num_rounds"]:
                p.participant.vars["dPGG_payoff"] = c(p.stock).to_real_world_currency(group.session)
                p.participant.vars["showup_fee"] = group.session.config['participation_fee']


def start(player: Player):
    if player.participant.vars["is_residual_player"]:
        player.endowment == 0
        player.stock == 0
    else:
        if player.round_number == 1:
            player.endowment = Constants.initial_endowment
        else:
            player.endowment = int(player.in_round(player.round_number - 1).stock)
        player.participant.vars["endowments"].append(player.endowment)


def contribution_max(player: Player):
    if player.round_number == 1:
        return Constants.initial_endowment
    else:
        return player.in_round(player.round_number - 1).stock


def donation_max(player: Player):
    return player.stock


def make_donation(player: Player):
    player.payoff = player.payoff - player.donation
    player.participant.vars["donation"] = c(player.donation).to_real_world_currency(player.session)


def belief_bonus(player: Player):
    if player.participant.vars["belief_bonus"] >= 0:
        if not player.is_dropout:
            if player.round_number == player.session.config["num_rounds"]:
                player.payoff = player.payoff + player.participant.vars["belief_bonus"]


def waiting_too_long(player: Player):
    return time.time() - player.participant.vars['wait_page_arrival'] > Constants.patience * 60


# PAGES
class dPGG_InitialWaitPage(WaitPage):
    template_name = 'dPGG/dPGG_InitialWaitPage.html'
    group_by_arrival_time = True

    @staticmethod
    def is_displayed(player: Player):
        if player.round_number == 1:
            return True


class dPGG_Belief(Page):
    form_model = "player"
    form_fields = ["review_instructions", "review_contact", "belief"]
    timeout_seconds = Constants.timeout * 60

    @staticmethod
    def is_displayed(player: Player):
        if not player.participant.vars["is_residual_player"]:
            if player.session.config["belief_elicitation"]:
                if player.round_number == Constants.belief_elicitation_round:
                    return True

    @staticmethod
    def js_vars(player: Player):
        return dict(
            timeout=Constants.timeout,
            template="decision",
            current_round=player.round_number,
            endowments=player.participant.vars["endowments"],
            num_rounds=player.session.config["num_rounds"],
        )

    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        if timeout_happened:
            player.belief = 0
            player.participant.vars["is_dropout"] = True
            player.is_dropout = True
            player.group.bot_active = True


class dPGG_Decision(Page):
    form_model = "player"
    form_fields = ["review_instructions", "review_contact", "contribution"]

    @staticmethod
    def get_timeout_seconds(player: Player):
        if player.participant.vars.get("is_dropout"):
            return 1  # instant timeout, 1 second
        else:
            if player.round_number == 1:
                return 2.5 * Constants.timeout * 60
            else:
                return Constants.timeout * 60

    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        if timeout_happened:
            player.contribution = random.randint(0, player.endowment)
            player.participant.vars["is_dropout"] = True
            player.is_dropout = True
            player.group.bot_active = True

    @staticmethod
    def is_displayed(player: Player):
        if not player.participant.vars["is_residual_player"]:
            if player.round_number <= player.session.config["num_rounds"]:
                return True

    @staticmethod
    def vars_for_template(player: Player):
        EWE = 0
        diff = 0
        bot_active = False
        if player.round_number > 1:
            EWE = player.group.in_round(player.round_number - 1).EWE
            diff = player.in_round(player.round_number - 1).gain
            bot_active = player.group.in_round(player.round_number - 1).bot_active
        return dict(
            EWE=EWE,
            diff=diff,
            bot_active=bot_active,
            previous_round=player.round_number - 1,
            last_round=player.session.config["num_rounds"],
        )

    @staticmethod
    def js_vars(player: Player):
        timeout = Constants.timeout
        if player.round_number == 1:
            timeout = 2.5 * Constants.timeout
        return dict(
            timeout=timeout,
            template="decision",
            current_round=player.round_number,
            endowments=player.participant.vars["endowments"],
            num_rounds=player.session.config["num_rounds"],
        )


class ResultsWaitPage(WaitPage):
    @staticmethod
    def is_displayed(player: Player):
        if player.round_number <= player.session.config["num_rounds"]:
            return True

    after_all_players_arrive = "set_payoffs"


class dPGG_Results(Page):
    @staticmethod
    def is_displayed(player: Player):
        if not player.participant.vars["is_residual_player"]:
            if player.round_number >= player.session.config["num_rounds"]:
                return True

    @staticmethod
    def get_timeout_seconds(player: Player):
        if player.participant.vars.get("is_dropout"):
            return 1  # instant timeout, 1 second

    @staticmethod
    def vars_for_template(player: Player):
        return dict(
            is_residual_player=player.participant.vars["is_residual_player"],
            final_payoff=player.participant.payoff_plus_participation_fee().to_real_world_currency(
                player.session
            ),
        )

    @staticmethod
    def js_vars(player: Player):
        return dict(
            template="results",
            current_round=player.round_number,
            stock=player.participant.vars["stock"],
            num_rounds=player.session.config["num_rounds"],
        )


class dPGG_Comprehension(Page):
    form_model = "player"
    form_fields = ["comprehension"]

    @staticmethod
    def is_displayed(player: Player):
        if not player.participant.vars["is_residual_player"]:
            if player.round_number >= player.session.config["num_rounds"]:
                return True

    @staticmethod
    def get_timeout_seconds(player: Player):
        if player.participant.vars.get("is_dropout"):
            return 1  # instant timeout, 1 second


class dPGG_Donation(Page):
    form_model = "player"
    form_fields = ["donation"]

    @staticmethod
    def is_displayed(player: Player):
        if not player.participant.vars["is_residual_player"]:
            if player.round_number >= player.session.config["num_rounds"]:
                return True

    @staticmethod
    def js_vars(player: Player):
        return dict(
            exchange_rate=player.session.config["real_world_currency_per_point"],
        )

    @staticmethod
    def get_timeout_seconds(player: Player):
        if player.participant.vars.get("is_dropout"):
            return 1  # instant timeout, 1 second

    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        make_donation(player)
        belief_bonus(player)

    @staticmethod
    def app_after_this_page(player: Player, upcoming_apps):
        if player.round_number >= player.session.config["num_rounds"]:
            return upcoming_apps[0]


page_sequence = [
    dPGG_InitialWaitPage,
    dPGG_Belief,
    dPGG_Decision,
    ResultsWaitPage,
    dPGG_Results,
    dPGG_Comprehension,
    dPGG_Donation,
]
