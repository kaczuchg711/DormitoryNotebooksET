# Generated by Django 3.0.8 on 2020-09-19 11:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rental', '0006_auto_20200821_1009'),
    ]

    operations = [
        migrations.AlterField(
            model_name='rentitem',
            name='returnHour',
            field=models.TimeField(default=None, null=True),
        ),
    ]