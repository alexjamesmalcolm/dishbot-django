# Generated by Django 3.1.4 on 2020-12-08 07:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dishbot', '0001_initial'),
    ]

    operations = [
        migrations.AddConstraint(
            model_name='house',
            constraint=models.UniqueConstraint(fields=('owned_by', 'name'), name='unique house names per user'),
        ),
    ]
