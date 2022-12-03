# Generated by Django 4.1.3 on 2022-12-02 07:36

import datetime
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('AdminPanel', '0002_claimgiftvoucher_flavours_giftvoucher_net_weight_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='claimgiftvoucher',
            name='GiftVoucher',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='AdminPanel.coupon'),
        ),
        migrations.AddField(
            model_name='claimgiftvoucher',
            name='redeemed',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='giftvoucher',
            name='bound',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='giftvoucher',
            name='code',
            field=models.CharField(blank=True, max_length=8, null=True, unique=True),
        ),
        migrations.AddField(
            model_name='giftvoucher',
            name='created',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='giftvoucher',
            name='expires',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='giftvoucher',
            name='percentage',
            field=models.DecimalField(decimal_places=2, default=1.0, max_digits=5),
        ),
        migrations.AddField(
            model_name='giftvoucher',
            name='repeat',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='giftvoucher',
            name='type',
            field=models.CharField(choices=[('percent', 'percent'), ('value', 'value')], default=datetime.datetime(2022, 12, 2, 7, 36, 4, 662148, tzinfo=datetime.timezone.utc), max_length=16),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='giftvoucher',
            name='updated',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AddField(
            model_name='news',
            name='Title',
            field=models.CharField(default=None, max_length=100),
        ),
        migrations.AddField(
            model_name='product',
            name='After_Coupoun_Price',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='product',
            name='After_GiftVoucher',
            field=models.IntegerField(blank=True, default=None, null=True),
        ),
        migrations.AddField(
            model_name='stores',
            name='LicenceNo',
            field=models.CharField(default=None, max_length=50, unique=True),
        ),
    ]