# Generated by Django 4.0.6 on 2022-10-03 08:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('scrapper', '0006_samutechcategories2_product_tag'),
    ]

    operations = [
        migrations.AddField(
            model_name='samutechcategories2',
            name='product_position',
            field=models.TextField(blank=True, null=True),
        ),
    ]
