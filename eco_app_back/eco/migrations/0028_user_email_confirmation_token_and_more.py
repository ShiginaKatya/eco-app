# Generated by Django 5.1.7 on 2025-04-22 13:02

import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('eco', '0027_userplan_is_done'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='email_confirmation_token',
            field=models.UUIDField(default=uuid.uuid4, editable=False),
        ),
        migrations.AddField(
            model_name='user',
            name='is_email_confirmed',
            field=models.BooleanField(default=False),
        ),
    ]
