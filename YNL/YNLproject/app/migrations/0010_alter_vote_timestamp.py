# Generated by Django 4.2.11 on 2024-07-31 15:34

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0009_remove_choice_name_choice_text_alter_poll_name_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='vote',
            name='timestamp',
            field=models.DateTimeField(default=datetime.datetime(2024, 7, 31, 15, 34, 54, 758106, tzinfo=datetime.timezone.utc)),
        ),
    ]
