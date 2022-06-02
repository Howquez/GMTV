from os import environ

SESSION_CONFIGS = [
    dict(
        name="GMTV",
        app_sequence=["A_Intro", "B_GMTV", "D_Outro"],
        num_demo_participants=2,
    ),
    dict(
        name="Clubs",
        app_sequence=["A_Intro", "B_Clubs", "D_Outro"],
        num_demo_participants=2,
    ),
    dict(
        name="EWE",
        app_sequence=["A_Intro", "B_EWE", "D_Outro"],
        num_demo_participants=3,
        num_rounds=10,
        group_size=3,
        efficiency_factor=1.5,
        risk=0.2,
        damage=0.5,
        initial_endowment=20,
    ),
]

# if you set a property in SESSION_CONFIG_DEFAULTS, it will be inherited by all configs
# in SESSION_CONFIGS, except those that explicitly override it.
# the session config can be accessed from methods in your apps as self.session.config,
# e.g. self.session.config['participation_fee']

SESSION_CONFIG_DEFAULTS = dict(
    real_world_currency_per_point=0.10,
    participation_fee=2.00,
    doc=""
)

PARTICIPANT_FIELDS = ["wait_page_arrival",
                      "waited_too_long",
                      "stock",
                      "euros",
                      "showup_fee",
                      "dPGG_payoff"]
SESSION_FIELDS = []

# ISO-639 code
# for example: de, fr, ja, ko, zh-hans
LANGUAGE_CODE = "en"

# e.g. EUR, GBP, CNY, JPY
REAL_WORLD_CURRENCY_CODE = "EUR"
USE_POINTS = True

ADMIN_USERNAME = 'admin'
# for security, best to set admin password in an environment variable
ADMIN_PASSWORD = environ.get('OTREE_ADMIN_PASSWORD')

DEMO_PAGE_INTRO_HTML = """ """

SECRET_KEY = '2501627228529'
