# Generated by Django 4.1 on 2022-09-05 18:30

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("word_lists", "0002_alter_wordlists_word"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="wordlists",
            options={"ordering": ["list_name"], "verbose_name_plural": "word_lists"},
        ),
    ]