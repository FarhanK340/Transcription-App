# Generated by Django 5.0.7 on 2024-07-25 14:09

import transcriptionApp.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('transcriptionApp', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='audiofile',
            name='audio',
            field=models.FileField(upload_to='audio/', validators=[transcriptionApp.validators.AudioFileValidator()]),
        ),
    ]
