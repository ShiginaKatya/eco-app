# Generated by Django 5.1.7 on 2025-04-01 11:18

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('eco', '0019_alter_usertask_challenge'),
    ]

    operations = [
        migrations.CreateModel(
            name='Level',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255, verbose_name='Название уровня')),
                ('description', models.TextField(null=True, verbose_name='Описание уровня')),
                ('min_points', models.PositiveIntegerField(verbose_name='Минимальное кол-во баллов')),
            ],
            options={
                'verbose_name': 'Уровень',
                'verbose_name_plural': 'Уровни',
            },
        ),
        migrations.AlterModelOptions(
            name='userchallenge',
            options={'verbose_name': 'Челлендж пользователя', 'verbose_name_plural': 'Челленджи пользователей'},
        ),
        migrations.AlterField(
            model_name='usertask',
            name='challenge',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='tasks', to='eco.userchallenge', verbose_name='Челлендж'),
        ),
        migrations.CreateModel(
            name='UserStat',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('points', models.PositiveIntegerField(default=0, verbose_name='Баллы')),
                ('level', models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to='eco.level', verbose_name='Уровень')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL, verbose_name='Пользователь')),
            ],
            options={
                'verbose_name': 'Статистика пользователя',
                'verbose_name_plural': 'Статистика пользователей',
            },
        ),
    ]
