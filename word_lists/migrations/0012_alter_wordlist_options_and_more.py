# Generated by Django 4.1 on 2022-09-29 22:04

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("word_lists", "0011_alter_wordlist_words"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="wordlist",
            options={
                "ordering": ["name"],
                "verbose_name": "word_list",
                "verbose_name_plural": "word_lists",
            },
        ),
        migrations.RenameField(
            model_name="wordlist",
            old_name="list_name",
            new_name="name",
        ),
        migrations.AlterUniqueTogether(
            name="wordlist",
            unique_together={("name", "user")},
        ),
    ]