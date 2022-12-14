# Generated by Django 4.1.1 on 2022-10-12 12:00

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ("chats", "0006_alter_chat_id"),
    ]

    operations = [
        migrations.AlterField(
            model_name="chat",
            name="id",
            field=models.UUIDField(
                default=uuid.uuid4, editable=False, primary_key=True, serialize=False
            ),
        ),
        migrations.AlterField(
            model_name="message",
            name="chat",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="messages",
                to="chats.chat",
            ),
        ),
    ]
