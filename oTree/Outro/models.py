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
    PQ07 = models.IntegerField(widget=widgets.RadioSelect, choices=[0, 1, 2, 3, 4, 5, 6], label="Familie spielt eine wichtige Rolle in meinem Leben.", doc="Family plays a very important role in my life")
    PQ08 = models.IntegerField(widget=widgets.RadioSelect, choices=[0, 1, 2, 3, 4, 5, 6], label="Freunde spielt eine wichtige Rolle in meinem Leben.", doc="Friends play a very important role in my life")
    PQ09 = models.IntegerField(widget=widgets.RadioSelect, choices=[0, 1, 2, 3, 4, 5, 6], label="Religion spielt eine wichtige Rolle in meinem Leben.", doc="Religion plays a very important role in my life")
    PQ10 = models.IntegerField(widget=widgets.RadioSelect, choices=[0, 1, 2, 3, 4, 5, 6], label="Politik spielt eine wichtige Rolle in meinem Leben.", doc="Politics plays a very important role in my life")
    PQ11 = models.IntegerField(widget=widgets.RadioSelect, choices=[0, 1, 2, 3, 4, 5, 6], label="Grundsätzlich kann man anderen vertrauen.", doc="Generally, most people can be trusted")
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

    Education = models.StringField(doc="Respondent's highest educational degree",
                                   label="Welchen beruflichen Ausbildungsabbschluss haben Sie?",
                                   choices=[
                                       ["student", "Ich bin noch in beruflicher Ausbildung (Studium oder Ausbildung)"],
                                       ["none",
                                        "Ich habe keinen beruflichen Abschluss und bin nicht in beruflicher Ausbildung"],
                                       ["apprenticeship",
                                        "Ich habe eine beruflich-betriebliche Berufsausbildung (Lehre) abgeschlossen"],
                                       ["highschool",
                                        "Ich habe eine beruflich-schulische Ausbildung (Berufsfachschule, Handelsschule) abgeschlossen"],
                                       ["applied highschool",
                                        "Ich habe eine Ausbildung an einer Fachschule, Meister-, Technikerschule, Berufs- oder Fachakademie abgeschlossen"],
                                       ["applied uni", "Ich habe einen Fachhochschulabschluss"],
                                       ["uni", "Ich habe einen Hochschulabschluss"]
                                   ],
                                   widget=widgets.RadioSelect)

    Income = models.IntegerField(doc="Respondent's income",
                                 label="Bitte nennen Sie Ihr ungefähres jährliches Nettoeinkommen.",
                                 blank=True)

    # Task Comprehension
    Comprehension = models.StringField(doc="Respondent's understanding of the tasks",
                                       label="Haben Sie die Aufgaben gut verstanden?",
                                       choices=[
                                           ["no", "Nein"],
                                           ["rather not", "Eher nicht"],
                                           ["rather yes", "Eher schon"],
                                           ["yes", "Ja"]
                                       ],
                                       widget=widgets.RadioSelect)

    # CLICCS common questions
    CLICCS1 = models.LongStringField(doc="CLICCS' common question #1",
                                     label="Was sehen Sie als größte Herausforderung in Bezug auf ein sich wandelndes Klima?",
                                     blank=True)
    CLICCS2 = models.LongStringField(doc="CLICCS' common question #2",
                                     label="Wie gehen Sie damit um?",
                                     blank=True)
