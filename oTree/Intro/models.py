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


author = 'Your name here'

doc = """
Your app description
"""


class Constants(BaseConstants):
    name_in_url = 'Intro'
    players_per_group = None
    num_rounds = 1
    group_size = 3
    num_others_per_group = group_size - 1
    initial_endowment = 20
    efficiency_factor = 1.25 # (MPCR) Marginal Per Capita Return per round
    rate_of_return = (efficiency_factor - 1)*100


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    pass
