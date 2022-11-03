from otree.api import *
import time


doc = """
Your app description
"""


class C(BaseConstants):
    NAME_IN_URL = 'A_Intro'
    PLAYERS_PER_GROUP = None
    NUM_ROUNDS = 1
    EARNINGS_TEMPLATE = "A_Intro/C_Earnings.html"
    SHOCKS_TEMPLATE = "A_Intro/D_Shocks.html"
    DEMO_TEMPLATE = "A_Intro/E_Demo.html"


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    formula_shown = models.BooleanField(doc="True if participant wanted to see the formula that explains earnings.",
                                        initial=False)


# PAGES
class A_Welcome(Page):
    pass


class B_Instructions(Page):
    form_model = "player"
    form_fields = ["formula_shown"]
    @staticmethod
    def before_next_page(player, timeout_happened):
        player.participant.waited_too_long = False
        player.participant.wait_page_arrival = time.time()

    @staticmethod
    def vars_for_template(player: Player):
        return dict(
            redirect="",
            damage=int(player.session.config["damage"]*100),
            risk=int(player.session.config["risk"]*100),
            group_members=player.session.config["group_size"] - 1,
            min_mpcr=round((player.session.config["efficiency_factor"]/player.session.config["group_size"] - player.session.config["risk"]*player.session.config["damage"])*100, 1),
            max_mpcr=round((player.session.config["efficiency_factor"]/player.session.config["group_size"])*100, 1),
        )


page_sequence = [A_Welcome,
                 B_Instructions]
