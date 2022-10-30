# Generated by Django 4.1 on 2022-10-17 19:51

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ("word_lists", "0004_alter_wordslist_options"),
    ]

    operations = [
        migrations.AlterField(
            model_name="wordslist",
            name="share_id",
            field=models.CharField(
                default=uuid.uuid4, editable=False, max_length=50, unique=True
            ),
        ),
    ]