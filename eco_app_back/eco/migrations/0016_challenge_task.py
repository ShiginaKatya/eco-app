# Generated by Django 5.1.7 on 2025-03-29 21:01

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('eco', '0015_achievement_userachievement'),
    ]

    operations = [
        migrations.CreateModel(
            name='Challenge',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255, verbose_name='Название челленджа')),
                ('goal', models.CharField(max_length=255, verbose_name='Цель')),
                ('description', models.TextField(null=True, verbose_name='Описание')),
                ('start_date', models.DateField(null=True, verbose_name='Дата начала')),
                ('finish_date', models.DateField(null=True, verbose_name='Дата окончания')),
                ('status', models.BooleanField(default=True, verbose_name='Доступен')),
                ('achievement', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='eco.achievement', verbose_name='Награда')),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='eco.category', verbose_name='Категория')),
            ],
            options={
                'verbose_name': 'Челлендж',
                'verbose_name_plural': 'Челленджи',
            },
        ),
        migrations.CreateModel(
            name='Task',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255, verbose_name='Задание')),
                ('challenge', models.ManyToManyField(to='eco.challenge', verbose_name='Челлендж')),
            ],
            options={
                'verbose_name': 'Задание',
                'verbose_name_plural': 'Задания',
            },
        ),
    ]
