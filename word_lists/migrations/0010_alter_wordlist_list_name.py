# Generated by Django 4.1 on 2022-09-29 21:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("word_lists", "0009_remove_wordlist_unique_user_list_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="wordlist",
            name="list_name",
            field=models.CharField(max_length=50),
        ),
    ]
