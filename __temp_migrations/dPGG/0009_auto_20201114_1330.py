# Generated by Django 2.2.12 on 2020-11-14 12:30

from django.db import migrations
import otree.db.models


class Migration(migrations.Migration):

    dependencies = [
        ('dPGG', '0008_player_gain'),
    ]

    operations = [
        migrations.AlterField(
            model_name='player',
            name='endowment',
            field=otree.db.models.CurrencyField(null=True),
        ),
    ]
