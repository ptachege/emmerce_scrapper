# Generated by Django 4.0.6 on 2022-07-25 22:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Opalnet', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='OpalnetProductLinks',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('link', models.CharField(blank=True, max_length=2000, null=True, unique=True)),
                ('crawled', models.BooleanField(default=False)),
            ],
            options={
                'verbose_name': 'OpalnetProductLinks',
                'verbose_name_plural': 'OpalnetProductLinks',
            },
        ),
    ]
