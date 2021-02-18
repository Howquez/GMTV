from otree.api import Currency as c, currency_range
from ._builtin import Page, WaitPage
from .models import Constants


class Outro_Covariates(Page):
    form_model = "player"
    form_fields = ["Age", "Gender", "Education", "Income", "Comprehension"]


class Outro_CLICCS(Page):
    form_model = "player"
    form_fields = ["CLICCS1", "CLICCS2"]



class Outro_Results(Page):
    def vars_for_template(self):
        return dict(
            is_residual_player=self.participant.vars["is_residual_player"],
            final_payoff=self.participant.payoff_plus_participation_fee().to_real_world_currency(self.session),
        )

    def js_vars(self):
        return dict(
            flat_fee=self.session.config["participation_fee"],
            exchange_rate=self.session.config["real_world_currency_per_point"],
            template="results",
            current_round=self.session.config["num_rounds"],
            stock=self.participant.vars["stock"],
        )


page_sequence = [Outro_Covariates, Outro_CLICCS, Outro_Results]
