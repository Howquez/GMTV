from otree.api import *


author = "Hauke Roggenkamp"
doc = """
Elicit covariates and display results
"""


class Constants(BaseConstants):
    name_in_url = 'Outro'
    players_per_group = None
    num_rounds = 1


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    # Gächter et al's (2017, JPE) Personality Questions
    PQ01 = models.IntegerField(
        widget=widgets.RadioSelect,
        choices=[0, 1, 2, 3, 4, 5, 6],
        label="Ich kann schnell denken.",
        doc="I am a quick thinker",
    )
    PQ02 = models.IntegerField(
        widget=widgets.RadioSelect,
        choices=[0, 1, 2, 3, 4, 5, 6],
        label="Ich fühle mich schnell angegriffen.",
        doc="I get easily offended",
    )
    PQ03 = models.IntegerField(
        widget=widgets.RadioSelect,
        choices=[0, 1, 2, 3, 4, 5, 6],
        label="Ich bin sehr zufrieden mit mir.",
        doc="I am very satisfied with myself",
    )
    PQ04 = models.IntegerField(
        widget=widgets.RadioSelect,
        choices=[0, 1, 2, 3, 4, 5, 6],
        label="Ich bin sehr auf andere angewiesen.",
        doc="I am very dependent on others",
    )
    PQ05 = models.IntegerField(
        widget=widgets.RadioSelect,
        choices=[0, 1, 2, 3, 4, 5, 6],
        label="Ich bin grundsätzlich glücklich.",
        doc="Generally speaking, I am happy",
    )
    PQ06 = models.IntegerField(
        widget=widgets.RadioSelect,
        choices=[0, 1, 2, 3, 4, 5, 6],
        label="Arbeit spielt eine wichtige Rolle in meinem Leben.",
        doc="Work plays a very important role in my life",
    )
    PQ07 = models.IntegerField(
        widget=widgets.RadioSelect,
        choices=[0, 1, 2, 3, 4, 5, 6],
        label="Familie spielt eine sehr wichtige Rolle in meinem Leben.",
        doc="Family plays a very important role in my life",
    )
    PQ08 = models.IntegerField(
        widget=widgets.RadioSelect,
        choices=[0, 1, 2, 3, 4, 5, 6],
        label="Freunde spielen eine sehr wichtige Rolle in meinem Leben.",
        doc="Friends play a very important role in my life",
    )
    PQ09 = models.IntegerField(
        widget=widgets.RadioSelect,
        choices=[0, 1, 2, 3, 4, 5, 6],
        label="Religion spielt eine sehr wichtige Rolle in meinem Leben.",
        doc="Religion plays a very important role in my life",
    )
    PQ10 = models.IntegerField(
        widget=widgets.RadioSelect,
        choices=[0, 1, 2, 3, 4, 5, 6],
        label="Politik spielt eine sehr wichtige Rolle in meinem Leben.",
        doc="Politics plays a very important role in my life",
    )
    PQ11 = models.IntegerField(
        widget=widgets.RadioSelect,
        choices=[0, 1, 2, 3, 4, 5, 6],
        label="Grundsätzlich kann man anderen vertrauen.",
        doc="Generally, others can be trusted",
    )
    PQ12 = models.IntegerField(
        widget=widgets.RadioSelect,
        choices=[0, 1, 2, 3, 4, 5, 6],
        label="Langfristig lohnt sich harte Arbeit.",
        doc="In the long run, hard work brings a better life",
    )
    PQ13 = models.IntegerField(
        widget=widgets.RadioSelect,
        choices=[0, 1, 2, 3, 4, 5, 6],
        label="Der Staat sollte sich darum kümmern, dass es den Leuten besser geht.",
        doc="The government should take responsibility that people are better provided for",
    )
    PQ14 = models.IntegerField(
        widget=widgets.RadioSelect,
        choices=[0, 1, 2, 3, 4, 5, 6],
        label="Einkommen sollten weniger ungleich sein.",
        doc="Incomes should be made more equal",
    )
    # Demographics
    Age = models.IntegerField(doc="Respondent's age", label="Wie alt sind Sie?")
    Gender = models.StringField(
        doc="Respondent's gender",
        label="Geschlecht",
        choices=[
            ["female", "weiblich"],
            ["male", "männlich"],
            ["diverse", "divers"],
            ["not specified", "keine Angabe"],
        ],
        widget=widgets.RadioSelect,
    )
    Education = models.IntegerField(
        doc="Respondent's highest educational degree",
        label="Bitte wählen Sie den höchsten Bildungsabschluss, den Sie bisher erreicht haben.",
        # "Welchen beruflichen Ausbildungsabbschluss haben Sie?",
        choices=[
            [0, "Schule beendet ohne Abschluss"],
            [1, "Noch Schüler"],
            [2, "Volks-, Hauptschulabschluss, Quali "],
            [3, "Mittlere Reife, Realschul- oder gleichwertiger Abschluss"],
            [4, "Abgeschlossene Lehre"],
            [5, "Fachabitur, Fachhochschulreife"],
            [6, "Abitur, Hochschulreife"],
            [7, "Fachhochschul-/Hochschulabschluss"],
            [8, "Anderer Abschluss"],
        ],
        widget=widgets.RadioSelect,
    )
    Income = models.IntegerField(
        doc="Respondent's income",
        label="Welches monatliche Budget haben Sie zur Verfügung? Bitte geben Sie Ihr eigenes monatliches Nettoeinkommen an.",
        choices=[
            [0, "0-500 €"],
            [1, "501-1.000 €"],
            [2, "1.001-2.000 €"],
            [3, "2.001-3.000 €"],
            [4, "3.001-4.000 €"],
            [5, "mehr als 4.000 €"],
            [9999, "keine Angabe"],
        ],
        blank=True,
        widget=widgets.RadioSelect,
    )
    # CLICCS common questions
    CLICCS1 = models.LongStringField(
        doc="CLICCS' common question #1",
        label="Was sehen Sie als größte Herausforderung in Bezug auf ein sich wandelndes Klima?",
        blank=True,
    )
    CLICCS2 = models.LongStringField(
        doc="CLICCS' common question #2", label="Wie gehen Sie damit um?", blank=True
    )
    # donation
    # donation = models.CurrencyField(doc="Donation",
    #                                 label="Möchten Sie einen Teil Ihres Verdienstes spenden? Wenn ja, wie viel?",
    #                                 blank=True)


# FUNCTIONS
# PAGES
class Outro_Personality(Page):
    form_model = "player"
    form_fields = [
        "PQ01",
        "PQ02",
        "PQ03",
        "PQ04",
        "PQ05",
        "PQ06",
        "PQ07",
        "PQ08",
        "PQ09",
        "PQ10",
        "PQ11",
        "PQ12",
        "PQ13",
        "PQ14",
    ]

    @staticmethod
    def vars_for_template(player: Player):
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

    @staticmethod
    def vars_for_template(player: Player):
        return dict(
            is_residual_player=player.participant.vars["is_residual_player"],
            final_payoff=player.participant.payoff_plus_participation_fee().to_real_world_currency(
                player.session
            ),
            payment_data_survey_link='https://www.limesurvey.uni-hamburg.de/index.php/162819?token='
            + str(player.participant.label),
        )

    @staticmethod
    def js_vars(player: Player):
        return dict(
            flat_fee=player.session.config["participation_fee"],
            exchange_rate=player.session.config["real_world_currency_per_point"],
            template="final",
            current_round=player.session.config["num_rounds"],
            euros=player.participant.vars["euros"],
            num_rounds=player.session.config["num_rounds"],
        )


page_sequence = [Outro_Personality, Outro_Covariates, Outro_CLICCS, Outro_Final]
