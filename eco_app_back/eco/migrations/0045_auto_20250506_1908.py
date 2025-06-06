# Generated by Django 5.1.7 on 2025-05-06 16:08

from django.db import migrations

def create_fts_table(apps, schema_editor):
    schema_editor.execute("CREATE VIRTUAL TABLE advice_search USING fts5(title, description)")

def insert_fts_table(apps, schema_editor):
    Advice = apps.get_model('eco', 'Advice')
    schema_editor.execute("INSERT INTO advice_search (title, description) SELECT title, description FROM eco_advice")

class Migration(migrations.Migration):

    dependencies = [
        ('eco', '0044_auto_20250506_1756'),
    ]

    operations = [
        migrations.RunSQL("DROP TABLE IF EXISTS advice_search"),
        migrations.RunPython(create_fts_table),
        migrations.RunPython(insert_fts_table),
    ]
