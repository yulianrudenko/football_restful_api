# Generated by Django 4.1.1 on 2022-10-16 20:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("authentication", "0005_alter_user_options_remove_user_last_login"),
    ]

    operations = [
        migrations.AlterField(
            model_name="user",
            name="auth_provider",
            field=models.CharField(
                choices=[
                    ("Facebook", "Facebook"),
                    ("Google", "Google"),
                    ("Email", "Email"),
                ],
                default="email",
                max_length=20,
            ),
        ),
    ]
