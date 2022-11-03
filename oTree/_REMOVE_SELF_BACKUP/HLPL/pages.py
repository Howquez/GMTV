from otree.api import Currency as c, currency_range
from ._builtin import Page, WaitPage
from .models import Constants


class HLPL_Decision(Page):
    form_model = "player"

    def is_displayed(self):
        if not self.participant.vars["is_residual_player"]:
            return True

    def get_form_fields(self):
        # unzip list of form_fields from <mpl_choices> list
        form_fields = [list(t) for t in zip(*self.participant.vars['mpl_choices'])][1]
        form_fields.extend(["review_instructions", "review_contact"])
        return form_fields

    def vars_for_template(self):
        return dict(
            choices=self.player.participant.vars["mpl_choices"]
        )

    def js_vars(self):
        return dict(
            template="risk",
        )

    def get_timeout_seconds(self):
        if self.participant.vars.get("is_dropout"):
            return 1  # instant timeout, 1 second

    def before_next_page(self):
        form_fields = [list(t) for t in zip(*self.participant.vars['mpl_choices'])][1]
        indices = [list(t) for t in zip(*self.participant.vars['mpl_choices'])][0]

        for j, choice in zip(indices, form_fields):
            choice_i = getattr(self.player, choice)
            self.participant.vars['mpl_choices_made'][j - 1] = choice_i

        # set payoff
        self.player.set_payoffs()
        # determine consistency
        self.player.set_consistency()
        # set switching row
        self.player.set_switching_row()

page_sequence = [HLPL_Decision]
