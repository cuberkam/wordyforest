# Generated by Django 4.1 on 2022-08-29 18:37

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("users", "0002_alter_customuser_email"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="customuser",
            name="first_name",
        ),
        migrations.RemoveField(
            model_name="customuser",
            name="last_name",
        ),
    ]
