from otree.api import Currency as c, currency_range
from ._builtin import Page, WaitPage
from .models import Constants
import random

class InitialWaitPage(WaitPage):
    group_by_arrival_time = True

    def is_displayed(self):
        if self.round_number == 1:
            return True


class dPGG_Decision(Page):
    form_model = "player"
    form_fields = ["contribution"]

    def get_timeout_seconds(self):
        if self.participant.vars.get("is_dropout"):
            return 1  # instant timeout, 1 second
        else:
            return 10#*60

    def before_next_page(self):
        if self.timeout_happened:
            self.player.contribution = random.randint(0, self.player.endowment)
            self.participant.vars["is_dropout"] = True
            self.player.is_dropout = True


    def is_displayed(self):
        if self.round_number <= self.session.config["num_rounds"]:
            return True

    def vars_for_template(self):
        disaster = 0
        diff = 0
        if self.round_number > 1:
            disaster = self.group.in_round(self.round_number - 1).disaster
            diff = self.player.in_round(self.round_number - 1).gain
        return dict(
            disaster = disaster,
            diff=diff,
        )

    def js_vars(self):
        return dict(
            template="decision",
            current_round=self.round_number,
            endowments=self.participant.vars["endowments"],
            num_rounds=self.session.config["num_rounds"],
        )

class ResultsWaitPage(WaitPage):
    # template_name = "dPGG/dPGG_Custom_Wait.html"

    def is_displayed(self):
        if self.round_number <= self.session.config["num_rounds"]:
            return True

    after_all_players_arrive = "set_payoffs"


class dPGG_Results(Page):
    def is_displayed(self):
        if self.round_number == self.session.config["num_rounds"]:
            return True

    def vars_for_template(self):
        return dict(
            final_payoff=self.participant.payoff_plus_participation_fee().to_real_world_currency(self.session),
        )

    def js_vars(self):
        return dict(
            flat_fee=self.session.config["participation_fee"],
            exchange_rate=self.session.config["real_world_currency_per_point"],
            template="results",
            current_round=self.round_number,
            stock=self.participant.vars["stock"],
        )



page_sequence = [InitialWaitPage,
                 dPGG_Decision,
                 ResultsWaitPage,
                 dPGG_Results]
