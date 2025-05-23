# Generated by Django 5.1.7 on 2025-04-29 19:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('eco', '0035_alter_advice_category_alter_advice_icon'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='status',
            field=models.CharField(choices=[('Назначено', 'Назначено'), ('Перенесено', 'Перенесено'), ('Завершено', 'Завершено'), ('Отменено', 'Отменено')], default='Назначено', max_length=255, verbose_name='Статус мероприятия'),
        ),
    ]
