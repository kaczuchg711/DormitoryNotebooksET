# Generated by Django 3.0.8 on 2020-08-21 09:56

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('rental', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='rentitem',
            old_name='id_Dorm',
            new_name='Dorm',
        ),
        migrations.RenameField(
            model_name='rentitem',
            old_name='id_User',
            new_name='User',
        ),
    ]