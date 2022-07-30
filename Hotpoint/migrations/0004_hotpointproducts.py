# Generated by Django 4.0.6 on 2022-07-21 13:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Hotpoint', '0003_alter_hotpointproductlinks_link'),
    ]

    operations = [
        migrations.CreateModel(
            name='HotpointProducts',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('product_name', models.CharField(blank=True, max_length=20000, null=True)),
                ('product_price', models.CharField(blank=True, max_length=20000, null=True)),
                ('regular_price', models.CharField(blank=True, max_length=20000, null=True)),
                ('brand', models.CharField(blank=True, max_length=20000, null=True)),
                ('upc', models.CharField(blank=True, max_length=20000, null=True)),
                ('sku', models.CharField(blank=True, max_length=20000, null=True)),
                ('product_link', models.CharField(blank=True, max_length=2000, null=True)),
            ],
            options={
                'verbose_name': 'HotpointProducts',
                'verbose_name_plural': 'HotpointProducts',
                'db_table': '',
                'managed': True,
            },
        ),
    ]
