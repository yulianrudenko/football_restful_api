# Generated by Django 4.1.1 on 2022-10-07 10:27

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("authentication", "0004_user_is_verified"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="user",
            options={"ordering": ["id"]},
        ),
        migrations.RemoveField(
            model_name="user",
            name="last_login",
        ),
    ]
