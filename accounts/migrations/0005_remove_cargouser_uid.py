# Generated by Django 4.2 on 2023-04-13 17:07

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0004_otpstorage_remove_cargouser_otp_cargouser_uid_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='cargouser',
            name='uid',
        ),
    ]
