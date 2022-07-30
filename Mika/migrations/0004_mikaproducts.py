# Generated by Django 4.0.6 on 2022-07-25 07:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Mika', '0003_alter_mikaproductlinks_options'),
    ]

    operations = [
        migrations.CreateModel(
            name='MikaProducts',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('product_name', models.CharField(blank=True, max_length=20000, null=True)),
                ('product_price', models.CharField(blank=True, max_length=20000, null=True)),
                ('regular_price', models.CharField(blank=True, max_length=20000, null=True)),
                ('stock_status', models.CharField(blank=True, max_length=20000, null=True)),
                ('sku', models.CharField(blank=True, max_length=20000, null=True)),
                ('product_link', models.CharField(blank=True, max_length=2000, null=True)),
            ],
        ),
    ]
