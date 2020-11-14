from otree.api import Currency as c, currency_range
from ._builtin import Page, WaitPage
from .models import Constants


class dPGG_Intro(Page):
    def is_displayed(self):
        if self.round_number == 1:
            return True

class dPGG_Decision(Page):
    form_model = "player"
    form_fields = ["contribution"]

    def is_displayed(self):
        if self.round_number <= self.session.config["num_rounds"]:
            return True

    def js_vars(self):
        return dict(
            template="decision",
            current_round=self.round_number,
            endowments=self.participant.vars["endowments"],
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



page_sequence = [dPGG_Intro, dPGG_Decision, ResultsWaitPage, dPGG_Results]
