# Generated by Django 4.1.3 on 2022-11-10 06:03

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('AdminPanel', '0007_alter_countries_country_alter_registeruser_gender'),
    ]

    operations = [
        migrations.RenameField(
            model_name='countries',
            old_name='Country',
            new_name='CountryName',
        ),
    ]