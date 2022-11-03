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


author = "Hauke Roggenkamp"

doc = """
Welcome participants, display instructions and comprehension questions.
"""


class Constants(BaseConstants):
    name_in_url = "A_Intro"
    players_per_group = None
    num_rounds = 1

    group_size = 4
    num_others_per_group = group_size - 1
    initial_endowment = 20
    efficiency_factor = 1.5 # (MPCR) Marginal Per Capita Return per round
    rate_of_return = (efficiency_factor - 1)*100


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    # Tracking Fields
    window_width = models.IntegerField(doc="Documents the respondent's browser window's width.")
    window_height = models.IntegerField(doc="Documents the respondent's browser window's height.")
    browser = models.StringField(doc="Documents the respondent's browser (incl. its version).")

    # Wrong Answers
    wrong_answer1_1 = models.IntegerField(doc="Counts the number of wrong guesses for CQ1_1.", initial=0)
    wrong_answer1_2 = models.IntegerField(doc="Counts the number of wrong guesses for CQ1_2.", initial=0)
    wrong_answer2_1 = models.IntegerField(doc="Counts the number of wrong guesses for CQ2_1.", initial=0)
    wrong_answer2_2 = models.IntegerField(doc="Counts the number of wrong guesses for CQ2_2.", initial=0)
    wrong_answer3_1 = models.IntegerField(doc="Counts the number of wrong guesses for CQ3_1.", initial=0)
    wrong_answer3_2 = models.IntegerField(doc="Counts the number of wrong guesses for CQ3_2.", initial=0)



    CQ1_1 = models.IntegerField(doc="Comprehension Question 1.1",
                                # initial=int(Constants.initial_endowment),
                                blank = True)
    def CQ1_1_error_message(self, value):
        if value != int(Constants.initial_endowment):
            self.wrong_answer1_1 += 1
            return "Leider falsch."

    CQ1_2 = models.IntegerField(doc="Comprehension Question 1.2",
                                # initial=int(Constants.initial_endowment),
                                blank = True)
    def CQ1_2_error_message(self, value):
        if value != int(Constants.initial_endowment):
            self.wrong_answer1_2 += 1
            return "Leider falsch."

    CQ2_1 = models.IntegerField(doc="Comprehension Question 2.1",
                                # initial=int(Constants.initial_endowment * Constants.efficiency_factor),
                                blank = True)
    def CQ2_1_error_message(self, value):
        if value != int(Constants.initial_endowment * Constants.efficiency_factor):
            self.wrong_answer2_1 += 1
            return "Leider falsch."

    CQ2_2 = models.IntegerField(doc="Comprehension Question 2.2",
                                # initial=int(Constants.initial_endowment * Constants.efficiency_factor),
                                blank = True)
    def CQ2_2_error_message(self, value):
        if value != int(Constants.initial_endowment * Constants.efficiency_factor):
            self.wrong_answer2_2 += 1
            return "Leider falsch."

    CQ3_1 = models.IntegerField(doc="Comprehension Question 3.1",
                                # initial=int(30 + Constants.efficiency_factor * 40 / Constants.group_size),
                                blank=True)
    def CQ3_1_error_message(self, value):
        if value != int(30 + Constants.efficiency_factor * 40 / Constants.group_size):
            self.wrong_answer3_1 += 1
            return "Leider falsch."

    CQ3_2 = models.BooleanField(doc="Comprehension Question 3.2",
                                widget=widgets.RadioSelect,
                                choices=[
                                    [False, "weiß nicht"],
                                    [True, "niedriger"],
                                    [False, "höher"]
                                ]
                                )
    def CQ3_2_error_message(self, value):
        if not value:
            self.wrong_answer3_2 += 1
            return "Leider falsch."