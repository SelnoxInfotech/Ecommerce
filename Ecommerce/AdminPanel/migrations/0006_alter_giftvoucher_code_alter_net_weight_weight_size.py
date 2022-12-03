# Generated by Django 4.1.3 on 2022-12-02 11:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('AdminPanel', '0005_alter_claimgiftvoucher_giftvoucher_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='giftvoucher',
            name='code',
            field=models.CharField(blank=True, max_length=8, null=True, unique=True),
        ),
        migrations.AlterField(
            model_name='net_weight',
            name='Weight_size',
            field=models.DecimalField(blank=True, decimal_places=2, default=0, max_digits=5, null=True),
        ),
    ]
