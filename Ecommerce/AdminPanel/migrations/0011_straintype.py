# Generated by Django 4.1.3 on 2022-11-10 07:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('AdminPanel', '0010_cities'),
    ]

    operations = [
        migrations.CreateModel(
            name='StrainType',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('strain', models.CharField(choices=[('N', 'None'), ('i', 'Indica'), ('s', 'Sativa'), ('h', 'hybrid'), ('c', 'CBD')], max_length=50)),
            ],
        ),
    ]
