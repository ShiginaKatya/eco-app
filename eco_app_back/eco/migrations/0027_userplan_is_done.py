# Generated by Django 5.1.7 on 2025-04-11 06:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('eco', '0026_alter_useranswer_options'),
    ]

    operations = [
        migrations.AddField(
            model_name='userplan',
            name='is_done',
            field=models.BooleanField(default=False, verbose_name='Статус завершения'),
        ),
    ]
