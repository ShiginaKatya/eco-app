# Generated by Django 5.1.7 on 2025-04-05 16:57

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('eco', '0023_useranswer'),
    ]

    operations = [
        migrations.CreateModel(
            name='Advice',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255, verbose_name='Cовет')),
                ('description', models.TextField(null=True, verbose_name='Описание')),
                ('icon', models.ImageField(upload_to='advices', verbose_name='Иконка совета')),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='eco.category', verbose_name='Категория')),
            ],
            options={
                'verbose_name': 'Совет',
                'verbose_name_plural': 'Советы',
            },
        ),
        migrations.CreateModel(
            name='Guide',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255, verbose_name='Руководство')),
                ('description', models.TextField(null=True, verbose_name='Описание')),
                ('icon', models.ImageField(upload_to='guides', verbose_name='Изображение для руководства')),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='eco.category', verbose_name='Категория')),
            ],
            options={
                'verbose_name': 'Руководство',
                'verbose_name_plural': 'Руководства',
            },
        ),
        migrations.CreateModel(
            name='Favorite',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('favorite_type', models.CharField(choices=[('A', 'Совет'), ('G', 'Руководство')], max_length=255, verbose_name='Тип')),
                ('advice', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='eco.advice', verbose_name='Совет')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Пользователь')),
                ('guide', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='eco.guide', verbose_name='Руководство')),
            ],
            options={
                'verbose_name': 'Избранное',
                'verbose_name_plural': 'Избранное пользователей',
            },
        ),
    ]
