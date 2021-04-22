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
    PQ01 = models.IntegerField(widget=widgets.RadioSelect, choices=[0, 1, 2, 3, 4, 5, 6], label="Ich kann schnell denken.", doc="I am a quick thinker")
    PQ02 = models.IntegerField(widget=widgets.RadioSelect, choices=[0, 1, 2, 3, 4, 5, 6], label="Ich fühle mich schnell angegriffen.", doc="I get easily offended")
    PQ03 = models.IntegerField(widget=widgets.RadioSelect, choices=[0, 1, 2, 3, 4, 5, 6], label="Ich bin sehr zufrieden mit mir.", doc="I am very satisfied with myself")
    PQ04 = models.IntegerField(widget=widgets.RadioSelect, choices=[0, 1, 2, 3, 4, 5, 6], label="Ich bin sehr auf andere angewiesen.", doc="I am very dependent on others")
    PQ05 = models.IntegerField(widget=widgets.RadioSelect, choices=[0, 1, 2, 3, 4, 5, 6], label="Ich bin grundsätzlich glücklich.", doc="Generally speaking, I am happy")
    PQ06 = models.IntegerField(widget=widgets.RadioSelect, choices=[0, 1, 2, 3, 4, 5, 6], label="Arbeit spielt eine wichtige Rolle in meinem Leben.", doc="Work plays a very important role in my life")
    PQ07 = models.IntegerField(widget=widgets.RadioSelect, choices=[0, 1, 2, 3, 4, 5, 6], label="Familie spielt eine sehr wichtige Rolle in meinem Leben.", doc="Family plays a very important role in my life")
    PQ08 = models.IntegerField(widget=widgets.RadioSelect, choices=[0, 1, 2, 3, 4, 5, 6], label="Freunde spielen eine sehr wichtige Rolle in meinem Leben.", doc="Friends play a very important role in my life")
    PQ09 = models.IntegerField(widget=widgets.RadioSelect, choices=[0, 1, 2, 3, 4, 5, 6], label="Religion spielt eine sehr wichtige Rolle in meinem Leben.", doc="Religion plays a very important role in my life")
    PQ10 = models.IntegerField(widget=widgets.RadioSelect, choices=[0, 1, 2, 3, 4, 5, 6], label="Politik spielt eine sehr wichtige Rolle in meinem Leben.", doc="Politics plays a very important role in my life")
    PQ11 = models.IntegerField(widget=widgets.RadioSelect, choices=[0, 1, 2, 3, 4, 5, 6], label="Grundsätzlich kann man anderen vertrauen.", doc="Generally, others can be trusted")
    PQ12 = models.IntegerField(widget=widgets.RadioSelect, choices=[0, 1, 2, 3, 4, 5, 6], label="Langfristig lohnt sich harte Arbeit.", doc="In the long run, hard work brings a better life")
    PQ13 = models.IntegerField(widget=widgets.RadioSelect, choices=[0, 1, 2, 3, 4, 5, 6], label="Der Staat sollte sich darum kümmern, dass es den Leuten besser geht.", doc="The government should take responsibility that people are better provided for")
    PQ14 = models.IntegerField(widget=widgets.RadioSelect, choices=[0, 1, 2, 3, 4, 5, 6], label="Einkommen sollten weniger ungleich sein.", doc="Incomes should be made more equal")

    # Demographics
    Age = models.IntegerField(doc="Respondent's age",
                              label="Wie alt sind Sie?")
    Gender = models.StringField(doc="Respondent's gender",
                                label="Geschlecht",
                                choices=[
                                    ["female", "weiblich"],
                                    ["male", "männlich"],
                                    ["diverse", "divers"],
                                    ["not specified", "keine Angabe"]
                                ],
                                widget=widgets.RadioSelect)

    Education = models.IntegerField(doc="Respondent's highest educational degree",
                                    label="Bitte wählen Sie den höchsten Bildungsabschluss, den Sie bisher erreicht haben.",
                                    # "Welchen beruflichen Ausbildungsabbschluss haben Sie?",
                                    choices=[
                                        [0, "Schule beendet ohne Abschluss"],
                                        [1, "Noch Schüler"],
                                        [2, "Volks-, Hauptschulabschluss, Quali "],
                                        [3, "Mittlere Reife, Realschul- oder gleichwertiger Abschluss"],
                                        [4, "Abgeschlossene Lehre"],
                                        [5, "Fachabitur, Fachhochschulreife"],
                                        [6, "Fachhochschul-/Hochschulabschluss"],
                                        [7, "Abitur, Hochschulreife"],
                                        [8, "Anderer Abschluss"],
                                    ],
                                    widget=widgets.RadioSelect)

    Income = models.IntegerField(doc="Respondent's income",
                                 label="Welches monatliche Budget haben Sie zur Verfügung? Bitte geben Sie Ihr monatliches Nettoeinkommen an.",
                                 choices=[
                                     [0, "0-500 €"],
                                     [1, "501-1.000 €"],
                                     [2, "1.001-2.000 €"],
                                     [3, "2.001-3.000 €"],
                                     [4, "3.001-4.000 €"],
                                     [5, "mehr als 4.000 €"],
                                     [9999, "keine Angabe"]
                                 ],
                                 blank=True,
                                 widget=widgets.RadioSelect)

    # Task Comprehension
    Comprehension = models.IntegerField(doc="Respondent's understanding of the tasks",
                                       label="Haben Sie die Aufgabe (der letzten 10 Runden) gut verstanden?",
                                       choices=[
                                           [0, "Nein"],
                                           [1, "Eher nicht"],
                                           [2, "Eher schon"],
                                           [3, "Ja"]
                                       ],
                                       widget=widgets.RadioSelect)

    # CLICCS common questions
    CLICCS1 = models.LongStringField(doc="CLICCS' common question #1",
                                     label="Was sehen Sie als größte Herausforderung in Bezug auf ein sich wandelndes Klima?",
                                     blank=True)
    CLICCS2 = models.LongStringField(doc="CLICCS' common question #2",
                                     label="Wie gehen Sie damit um?",
                                     blank=True)
