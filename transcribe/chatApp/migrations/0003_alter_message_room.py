# Generated by Django 5.0.7 on 2024-07-31 11:05

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chatApp', '0002_rename_name_room_room_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='message',
            name='room',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='chatApp.room'),
        ),
    ]
