from otree.api import Currency as c, currency_range
from ._builtin import Page, WaitPage
from .models import Constants
import random

class dPGG_InitialWaitPage(WaitPage):
    template_name = 'dPGG/dPGG_InitialWaitPage.html'
    group_by_arrival_time = True

    def is_displayed(self):
        if self.round_number == 1:
            return True


class dPGG_Decision(Page):
    form_model = "player"
    form_fields = ["review_instructions", "contribution"]

    def get_timeout_seconds(self):
        if self.participant.vars.get("is_dropout"):
            return 1  # instant timeout, 1 second
        else:
            if self.round_number == 1:
                return 2 * Constants.timeout * 60
            else:
                return Constants.timeout * 60

    def before_next_page(self):
        if self.timeout_happened:
            self.player.contribution = random.randint(0, self.player.endowment)
            self.participant.vars["is_dropout"] = True
            self.player.is_dropout = True
            self.group.bot_active = True


    def is_displayed(self):
        if not self.participant.vars["is_residual_player"]:
            if self.round_number <= self.session.config["num_rounds"]:
                return True

    def vars_for_template(self):
        disaster = 0
        diff = 0
        bot_active = False
        if self.round_number > 1:
            disaster = self.group.in_round(self.round_number - 1).disaster
            diff = self.player.in_round(self.round_number - 1).gain
            bot_active = self.group.in_round(self.round_number - 1).bot_active
        return dict(
            disaster = disaster,
            diff=diff,
            bot_active=bot_active,
            previous_round=self.round_number - 1,
            last_round=self.session.config["num_rounds"]
        )

    def js_vars(self):
        return dict(
            template="decision",
            current_round=self.round_number,
            endowments=self.participant.vars["endowments"],
            num_rounds=self.session.config["num_rounds"],
        )


class dPGG_Belief(Page):
    form_model = "player"
    form_fields = ["review_instructions", "belief"]

    def is_displayed(self):
        if self.round_number == Constants.belief_elicitation_round:
            return True

    def js_vars(self):
        return dict(
            template="decision",
            current_round=self.round_number,
            endowments=self.participant.vars["endowments"],
            num_rounds=self.session.config["num_rounds"],
        )


class ResultsWaitPage(WaitPage):
    def is_displayed(self):
        if self.round_number <= self.session.config["num_rounds"]:
            return True

    def app_after_this_page(self, upcoming_apps):
        if self.round_number >= self.session.config["num_rounds"]:
            return upcoming_apps[0]

    after_all_players_arrive = "set_payoffs"




page_sequence = [dPGG_InitialWaitPage,
                 dPGG_Decision,
                 dPGG_Belief,
                 ResultsWaitPage]
