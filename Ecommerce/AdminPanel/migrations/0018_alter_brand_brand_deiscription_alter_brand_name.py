# Generated by Django 4.1.3 on 2022-11-10 11:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('AdminPanel', '0017_rename_productname_product_product_name_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='brand',
            name='Brand_deiscription',
            field=models.CharField(default=None, max_length=500),
        ),
        migrations.AlterField(
            model_name='brand',
            name='name',
            field=models.CharField(default=None, max_length=50),
        ),
    ]
