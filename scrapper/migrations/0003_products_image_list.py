# Generated by Django 4.0.6 on 2022-09-22 01:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('scrapper', '0002_products_long_description_products_short_description'),
    ]

    operations = [
        migrations.AddField(
            model_name='products',
            name='image_list',
            field=models.TextField(blank=True, null=True),
        ),
    ]
