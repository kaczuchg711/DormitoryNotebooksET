# Generated by Django 3.0.8 on 2021-01-20 12:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('breakdowns', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='breakdowns',
            name='rentalDate',
            field=models.DateField(default=None),
        ),
    ]
