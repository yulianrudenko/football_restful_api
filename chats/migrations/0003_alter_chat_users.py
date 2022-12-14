# Generated by Django 4.1.1 on 2022-10-09 21:37

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("chats", "0002_alter_chat_users"),
    ]

    operations = [
        migrations.AlterField(
            model_name="chat",
            name="users",
            field=models.ManyToManyField(
                blank=True, null=True, related_name="chats", to=settings.AUTH_USER_MODEL
            ),
        ),
    ]
