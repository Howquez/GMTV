from otree.api import *
import time


doc = """
Your app description
"""


class C(BaseConstants):
    NAME_IN_URL = 'A_Intro'
    PLAYERS_PER_GROUP = None
    NUM_ROUNDS = 1


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    pass


# PAGES
class A_Welcome(Page):
    pass


class B_Instructions(Page):
    @staticmethod
    def before_next_page(player, timeout_happened):
        player.participant.waited_too_long = False
        player.participant.wait_page_arrival = time.time()


page_sequence = [A_Welcome,
                 B_Instructions]
