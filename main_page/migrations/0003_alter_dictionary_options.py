# Generated by Django 4.1 on 2022-09-05 18:30

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("main_page", "0002_rename_worddict_dictionary"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="dictionary",
            options={"ordering": ["word"], "verbose_name_plural": "dictionaries"},
        ),
    ]