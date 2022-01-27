from otree.api import *
import time
import math

doc = """
Public Bads Game
"""


class C(BaseConstants):
    NAME_IN_URL = "Clubs"
    PLAYERS_PER_GROUP = 2
    NUM_ROUNDS = 10
    PATIENCE = 1
    PATIENCE_BONUS = 20
    ENDOWMENT = 20
    EFFICIENCY_FACTOR = 0.75
    TIMEOUT = 4


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    residual = models.BooleanField(initial=False, doc="if true, group is incomplete")
    club_size = models.IntegerField(doc="number of club members")
    threshold_contribution = models.IntegerField(doc="minimum contribution required to stay in the club", initial = 10)
    total_contribution = models.IntegerField(doc="sum of contributions in this round")
    average_contribution = models.FloatField(doc="average contribution in this round")
    individual_share = models.IntegerField(doc="individual share each player receives from this round's contributions")
    wealth = models.IntegerField(doc="sum of endowments at the beginning of a round")



class Player(BasePlayer):
    payoff_int = models.IntegerField(doc="payoffs as integers")
    wait_time_left = models.IntegerField(doc="denotes the time a player has to wait for others to arrive on WaitPage")
    join = models.StringField(doc="whether the player wants to join the club", initial = "", blank = True)
    member = models.BooleanField(doc="whether the player is a member the club", initial = False, blank = True)
    contribution = models.IntegerField(min=0, max=C.ENDOWMENT, doc="the player's contribution in this round")
    stock = models.IntegerField(doc="accumulated earnings of played rounds")


# FUNCTIONS
def waiting_too_long(player):
    participant = player.participant
    import time
    # assumes you set wait_page_arrival in PARTICIPANT_FIELDS.
    return time.time() - participant.wait_page_arrival > C.PATIENCE*60

def group_by_arrival_time_method(subsession, waiting_players):
    if len(waiting_players) >= C.PLAYERS_PER_GROUP:
        return waiting_players[:C.PLAYERS_PER_GROUP]
    for player in waiting_players:
        player.wait_time_left = int(math.ceil(C.PATIENCE - (time.time() - player.participant.wait_page_arrival) / 60))
        if waiting_too_long(player):
            player.participant.waited_too_long = True
            # make a single-player group.
            return [player]

def set_group_variables(group: Group):
    if len(group.get_players()) == C.PLAYERS_PER_GROUP:
        group.total_contribution = sum([p.contribution for p in group.get_players()])
        group.average_contribution = round(
            group.total_contribution / C.PLAYERS_PER_GROUP, 2
        )
        group.individual_share = int(
            math.ceil(
                group.total_contribution * C.EFFICIENCY_FACTOR / C.PLAYERS_PER_GROUP
            )
        )

def set_payoffs(group: Group):
    # membership status by choice
    for p in group.get_players(): # calculate player-level-variables
        if p.round_number > 1:
            p.member = p.in_round(p.round_number - 1).member
        if p.join == "Join":
            p.member = True
        elif p.join == "Leave":
            p.member = False
        # BEFORE payoffs are calculated check whether subject is allowed to stay in the club
        if p.contribution < group.threshold_contribution:
            p.member = False

    # calc payoffs
    set_group_variables(group)
    for p in group.get_players():
        p.payoff = int(math.ceil(C.ENDOWMENT + group.individual_share - p.contribution))
        p.payoff_int = int(p.payoff)
        if p.round_number == 1:
            p.stock = p.payoff_int
            p.participant.stock = [p.stock]
        else:
            p.stock = int(p.in_round(p.round_number - 1).stock + p.payoff)

        p.participant.stock.append(p.stock)

        if p.contribution < group.threshold_contribution:
            p.member = False



# PAGES
class A_InitialWaitPage(WaitPage):
    template_name = "B_Clubs/A_InitialWaitPage.html"
    group_by_arrival_time = True

    @staticmethod
    def is_displayed(player):
        return player.round_number == 1

    @staticmethod
    def app_after_this_page(player, upcoming_apps):
        if player.participant.waited_too_long == True:
            return upcoming_apps[0]


class B_Join(Page):
    form_model = "player"
    form_fields = ["join"]

    @staticmethod
    def vars_for_template(player: Player):
        earnings = 0
        diff = 0
        bot_active = False
        if player.round_number > 1:
            earnings = player.in_round(player.round_number - 1).stock
            diff = player.in_round(player.round_number - 1).payoff
        return dict(
            redirect="",
            bot_active=bot_active,
            previous_round=player.round_number - 1,
        )

class C_Contribution(Page):
    form_model = "player"
    form_fields = ["join", "contribution"]

    @staticmethod
    def vars_for_template(player: Player):
        is_member = False
        earnings = 0
        diff = 0
        bot_active = False
        if player.round_number > 1:
            earnings = player.in_round(player.round_number - 1).stock
            diff = player.in_round(player.round_number - 1).payoff
            if player.in_round(player.round_number - 1).member:
                is_member = True
        return dict(
            redirect="",
            is_member=is_member,
            earnings=earnings,
            diff=diff,
            bot_active=bot_active,
            previous_round=player.round_number - 1,
        )

    @staticmethod
    def js_vars(player: Player):
        timeout = C.TIMEOUT
        if player.round_number == 1:
            timeout = 2.5 * C.TIMEOUT
            stock = C.ENDOWMENT
        else:
            stock = player.participant.stock
        return dict(
            stock=stock,
            timeout=timeout,
            template="decision",
            current_round=player.round_number,
            num_rounds=C.NUM_ROUNDS,
        )


class D_ResultsWaitPage(WaitPage):
    after_all_players_arrive = "set_payoffs"


class E_Results(Page):
    @staticmethod
    def is_displayed(player):
        if player.round_number == C.NUM_ROUNDS:
            return True


page_sequence = [A_InitialWaitPage,
                 # B_Join,
                 C_Contribution,
                 D_ResultsWaitPage,
                 E_Results]
