# Generated by Django 4.0.6 on 2022-09-22 01:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('scrapper', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='products',
            name='long_description',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='products',
            name='short_description',
            field=models.TextField(blank=True, null=True),
        ),
    ]
