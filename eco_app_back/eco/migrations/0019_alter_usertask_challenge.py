# Generated by Django 5.1.7 on 2025-03-30 21:27

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('eco', '0018_alter_userhabit_habit_userchallenge_usertask'),
    ]

    operations = [
        migrations.AlterField(
            model_name='usertask',
            name='challenge',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='eco.userchallenge', verbose_name='Челлендж'),
        ),
    ]
