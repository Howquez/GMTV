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
    ENDOWMENT = 60
    EFFICIENCY_FACTOR = 1
    TIMEOUT = 4
    MEMBER_ROLE = "Member"
    OUTSIDER_ROLE = "Outsider"



class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    residual = models.BooleanField(initial=False, doc="if true, group is incomplete")
    threshold_investment = models.IntegerField(doc="maximum investment allowed to stay in the club", initial = 10)
    total_investment = models.IntegerField(doc="sum of all investments in this period")
    average_investment = models.FloatField(doc="average investment in this round")

    club_size = models.IntegerField(doc="number of club members", initial = 0)
    club_investment = models.IntegerField(doc="sum of club members' investments in this period", initial = 0)
    average_club_investment = models.IntegerField(doc="average of club members' investments in this period", initial = 0)
    average_club_payoff = models.IntegerField(doc="average of club members' payoff in this period", initial = 0)

    outsiders_size = models.IntegerField(doc="number of outsiders", initial = 0)
    outsiders_investment = models.IntegerField(doc="sum of outsiders' investments in this period", initial = 0)
    average_outsider_investment = models.IntegerField(doc="average of outsiders' investments in this period", initial = 0)
    average_outsider_payoff = models.IntegerField(doc="average of outsiders' payoff in this period", initial = 0)


wealth = models.IntegerField(doc="sum of endowments at the beginning of a round")



class Player(BasePlayer):
    payoff_int = models.IntegerField(doc="payoffs as integers")
    wait_time_left = models.IntegerField(doc="denotes the time a player has to wait for others to arrive on WaitPage")
    join = models.StringField(doc="whether the player wants to join the club", initial = "", blank = True)
    member = models.BooleanField(doc="whether the player is a member the club", initial = False, blank = True)
    investment = models.IntegerField(min=0, max=C.ENDOWMENT, doc="the player's investment in this round")
    others_externalities = models.IntegerField(doc="amount a player is deducted due to the group members' investments")
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
        group.total_investment = sum([p.investment for p in group.get_players()])
        group.average_investment = round(
            group.total_investment / C.PLAYERS_PER_GROUP, 2
        )

def set_club_variables(group: Group):
    if len(group.get_players()) == C.PLAYERS_PER_GROUP:
        club_payoffs = 0
        outsider_payoffs = 0
        for p in group.get_players():
            if p.member:
                group.club_size += 1
                group.club_investment += p.investment
                club_payoffs += p.payoff
            else:
                group.outsiders_size += 1
                group.outsiders_investment += p.investment
                outsider_payoffs += p.payoff

        group.average_club_investment = int(math.floor(group.club_investment / group.club_size)) if group.club_size > 0 else 0
        group.average_club_payoff = int(math.floor(club_payoffs / group.club_size)) if group.club_size > 0 else 0
        group.average_outsider_investment = int(math.floor(group.outsiders_investment / group.outsiders_size)) if group.outsiders_size > 0 else 0
        group.average_outsider_payoff = int(math.floor(outsider_payoffs / group.outsiders_size)) if group.outsiders_size > 0 else 0

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
        if p.investment >= group.threshold_investment:
            p.member = False

    # calc payoffs
    set_group_variables(group)
    for p in group.get_players():
        p.others_externalities = int(math.floor((group.total_investment - p.investment) * 0.75))
        p.payoff = int(math.ceil(p.investment - p.others_externalities + (C.ENDOWMENT - p.investment) * 0.5))
        p.payoff_int = int(p.payoff)
        if p.round_number == 1:
            p.stock = p.payoff_int
            p.participant.stock = [p.stock]
        else:
            p.stock = int(p.in_round(p.round_number - 1).stock + p.payoff)

        p.participant.stock.append(p.stock)
    set_club_variables(group)



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
    form_fields = ["join", "investment"]

    @staticmethod
    def vars_for_template(player: Player):

        is_member = False
        earnings = 0
        diff = 0
        bot_active = False

        club_size = 0
        club_investment = 0
        club_payoff = 0

        outsiders_size = 0
        outsiders_investment = 0
        outsiders_payoff = 0

        if player.round_number > 1:
            earnings = player.in_round(player.round_number - 1).stock
            diff = player.in_round(player.round_number - 1).payoff
            if player.in_round(player.round_number - 1).member:
                is_member = True

            club_size = player.group.in_round(player.round_number - 1).club_size
            club_investment = player.group.in_round(player.round_number - 1).average_club_investment
            club_payoff = player.group.in_round(player.round_number - 1).average_club_payoff

            outsiders_size = player.group.in_round(player.round_number - 1).outsiders_size
            outsiders_investment = player.group.in_round(player.round_number - 1).average_outsider_investment
            outsiders_payoff = player.group.in_round(player.round_number - 1).average_outsider_payoff

        return dict(
            redirect="",
            is_member=is_member,
            earnings=earnings,
            diff=diff,
            bot_active=bot_active,
            previous_round=player.round_number - 1,
            club_size=club_size,
            club_investment=club_investment,
            club_payoff=club_payoff,
            outsiders_size=outsiders_size,
            outsiders_investment=outsiders_investment,
            outsiders_payoff=outsiders_payoff
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
