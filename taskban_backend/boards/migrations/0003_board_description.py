# Generated by Django 3.2.12 on 2022-04-17 06:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('boards', '0002_auto_20220413_1733'),
    ]

    operations = [
        migrations.AddField(
            model_name='board',
            name='description',
            field=models.TextField(blank=True),
        ),
    ]
