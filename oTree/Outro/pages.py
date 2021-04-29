from otree.api import Currency as c, currency_range
from ._builtin import Page, WaitPage
from .models import Constants


class Outro_Personality(Page):
    form_model = "player"
    form_fields = ["PQ01", "PQ02", "PQ03", "PQ04", "PQ05",
                   "PQ06", "PQ07", "PQ08", "PQ09", "PQ10",
                   "PQ11", "PQ12", "PQ13", "PQ14"]

    def vars_for_template(self):
        return dict(
            choices=[0, 1, 2, 3, 4, 5, 6],
        )

class Outro_Covariates(Page):
    form_model = "player"
    form_fields = ["Age", "Gender", "Education", "Income"]


class Outro_CLICCS(Page):
    form_model = "player"
    form_fields = ["CLICCS1", "CLICCS2"]



class Outro_Final(Page):
    form_model = "player"
    form_fields = ["donation"]

    def vars_for_template(self):
        return dict(
            is_residual_player=self.participant.vars["is_residual_player"],
            final_payoff=self.participant.payoff_plus_participation_fee().to_real_world_currency(self.session),
        )

    def js_vars(self):
        return dict(
            flat_fee=self.session.config["participation_fee"],
            exchange_rate=self.session.config["real_world_currency_per_point"],
            template="final",
            current_round=self.session.config["num_rounds"],
            euros=self.participant.vars["euros"],
            num_rounds=self.session.config["num_rounds"],
        )


page_sequence = [Outro_Personality, Outro_Covariates, Outro_CLICCS, Outro_Final]
