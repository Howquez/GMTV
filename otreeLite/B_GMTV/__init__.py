from otree.api import *
import math
import time



doc = """
Your app description
"""

# MODELS
class C(BaseConstants):
    NAME_IN_URL = 'GMTV'
    PLAYERS_PER_GROUP = 2
    NUM_ROUNDS = 10
    PATIENCE = 1
    PATIENCE_BONUS = 20
    INITIAL_ENDOWMENT = 20
    EFFICIENCY_FACTOR = 1.5
    TIMEOUT = 4


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    residual = models.BooleanField(initial=False, doc="if true, group is incomplete")
    EWE = models.BooleanField(initial=False, doc="if true, extreme weather event occurred")
    total_contribution = models.IntegerField(doc="sum of contributions in this round")
    average_contribution = models.FloatField(doc="average contribution in this round")
    individual_share = models.IntegerField(doc="individual share each player receives from this round's contributions")
    wealth = models.IntegerField(doc="sum of endowments at the beginning of a round")


class Player(BasePlayer):
    wait_time_left = models.IntegerField(doc="denotes the time a player has to wait for others to arrive on WaitPage")
    endowment = models.IntegerField(doc="the player's endowment in this round (equals her stock of last round)")
    contribution = models.IntegerField(min=0, doc="the player's contribution in this round")
    stock = models.IntegerField(doc="accumulated earnings of played rounds")
    gain = models.IntegerField(doc="a round's earnings.")



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

def contribution_max(player: Player):
    if player.round_number == 1:
        return C.INITIAL_ENDOWMENT
    else:
        return int(math.ceil(player.in_round(player.round_number - 1).stock))

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
    set_group_variables(group)
    for p in group.get_players(): # calculate player-level-variables

        if p.round_number == 1:
            p.endowment = C.INITIAL_ENDOWMENT
            p.stock = p.endowment + group.individual_share - p.contribution
            p.gain = (p.stock - p.endowment)
            p.participant.stock = [20]
        else:
            p.endowment = int(math.ceil(p.in_round(p.round_number - 1).stock))

        p.stock = p.endowment + group.individual_share - p.contribution
        p.gain = (p.stock - p.endowment)
        p.participant.stock.append(p.stock)
        # p.participant.vars["stock"].append(p.stock) # vars for visualization?
        # p.participant.vars["euros"].append(cu(p.stock).to_real_world_currency(group.session))
        if p.round_number == 1:
            p.payoff = cu(p.stock)
        else:
            p.payoff = cu(p.gain)
        # store payoff in participant var to display it across apps
        if group.round_number == C.NUM_ROUNDS:
            p.participant.vars["dPGG_payoff"] = cu(p.stock).to_real_world_currency(group.session)
            p.participant.vars["showup_fee"] = group.session.config["participation_fee"]


# PAGES
class A_InitialWaitPage(WaitPage):
    template_name = "B_GMTV/A_InitialWaitPage.html"
    group_by_arrival_time = True

    @staticmethod
    def is_displayed(player):
        return player.round_number == 1

    @staticmethod
    def app_after_this_page(player, upcoming_apps):
        if player.participant.waited_too_long == True:
            return upcoming_apps[0]


class B_Decision(Page):
    form_model = "player"
    form_fields = ["contribution"]

    @staticmethod
    def vars_for_template(player: Player):
        endowment = C.INITIAL_ENDOWMENT
        diff = 0
        bot_active = False
        if player.round_number > 1:
            endowment = int(math.ceil(player.in_round(player.round_number - 1).stock))
            diff = player.in_round(player.round_number - 1).gain
        return dict(
            redirect="",
            endowment=endowment,
            diff=diff,
            bot_active=bot_active,
            previous_round=player.round_number - 1,
        )

    @staticmethod
    def js_vars(player: Player):
        timeout = C.TIMEOUT
        if player.round_number == 1:
            timeout = 2.5 * C.TIMEOUT
            stock = C.INITIAL_ENDOWMENT
        else:
            stock = player.participant.stock
        return dict(
            timeout=timeout,
            template="decision",
            current_round=player.round_number,
            stock=stock,
            num_rounds=C.NUM_ROUNDS,
        )


class C_ResultsWaitPage(WaitPage):
    after_all_players_arrive = "set_payoffs"


class D_Results(Page):
    @staticmethod
    def is_displayed(player):
        if player.round_number == C.NUM_ROUNDS:
            return True


page_sequence = [A_InitialWaitPage,
                 B_Decision,
                 C_ResultsWaitPage,
                 D_Results]
