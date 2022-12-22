# Generated by Django 4.1.4 on 2022-12-20 06:04

import ckeditor.fields
from django.db import migrations, models
import django.db.models.deletion
import phonenumber_field.modelfields


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Brand",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(default=None, max_length=50)),
                ("Brand_description", ckeditor.fields.RichTextField(default=None)),
                (
                    "Brand_Logo",
                    models.ImageField(default=None, upload_to="media/Brand"),
                ),
                (
                    "Status",
                    models.CharField(
                        choices=[("1", "Active"), ("0", "Hide")],
                        default=1,
                        max_length=20,
                    ),
                ),
                ("Link", models.URLField(blank=True, default=None)),
                ("created", models.DateTimeField(auto_now_add=True)),
                ("updated", models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name="Category",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=500)),
                (
                    "Status",
                    models.CharField(
                        choices=[("1", "Active"), ("0", "Hide")],
                        default=1,
                        max_length=20,
                    ),
                ),
                ("created", models.DateTimeField(auto_now_add=True)),
                ("updated", models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name="Cities",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("CityName", models.CharField(max_length=100)),
                (
                    "Status",
                    models.CharField(
                        choices=[("1", "Active"), ("0", "Hide")],
                        default=1,
                        max_length=20,
                    ),
                ),
                ("created", models.DateTimeField(auto_now_add=True)),
                ("updated", models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name="ClaimedCoupon",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("redeemed", models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name="ClaimGiftVoucher",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("redeemed", models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name="Countries",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("CountryName", models.CharField(max_length=100)),
                (
                    "Status",
                    models.CharField(
                        choices=[("1", "Active"), ("0", "Hide")],
                        default=1,
                        max_length=20,
                    ),
                ),
                ("created", models.DateTimeField(auto_now_add=True)),
                ("updated", models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name="Coupon",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("created", models.DateTimeField(auto_now_add=True)),
                ("updated", models.DateTimeField(auto_now=True)),
                ("code", models.CharField(max_length=64)),
                ("code_l", models.CharField(blank=True, max_length=64, unique=True)),
                (
                    "type",
                    models.CharField(
                        choices=[("percent", "percent"), ("value", "value")],
                        max_length=16,
                    ),
                ),
                ("expires", models.DateTimeField(blank=True, null=True)),
                (
                    "percentage",
                    models.DecimalField(decimal_places=2, default=1.0, max_digits=5),
                ),
                ("bound", models.BooleanField(default=False)),
                ("repeat", models.IntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name="Discount",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("Discount_value", models.IntegerField(default=0)),
                ("Discount_type", models.CharField(max_length=20)),
                (
                    "Status",
                    models.CharField(
                        choices=[("1", "Active"), ("0", "Hide")],
                        default=1,
                        max_length=20,
                    ),
                ),
                ("created", models.DateTimeField(auto_now_add=True)),
                ("updated", models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name="ExportFile",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("File", models.FileField(upload_to="excel")),
                ("created", models.DateTimeField(auto_now_add=True)),
                ("updated", models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name="Flavours",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("flavour_Name", models.CharField(default=None, max_length=50)),
                ("Price", models.IntegerField(default=0)),
                (
                    "FlavoursImage",
                    models.ImageField(default=None, upload_to="media/Products"),
                ),
                ("created", models.DateTimeField(auto_now_add=True)),
                ("updated", models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name="GiftVoucher",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("created", models.DateTimeField(auto_now_add=True)),
                ("updated", models.DateTimeField(auto_now=True)),
                (
                    "type",
                    models.CharField(
                        choices=[("percent", "percent"), ("value", "value")],
                        max_length=16,
                    ),
                ),
                ("expires", models.DateTimeField(blank=True, null=True)),
                (
                    "percentage",
                    models.DecimalField(decimal_places=2, default=0.0, max_digits=5),
                ),
                ("bound", models.BooleanField(default=False)),
                ("repeat", models.IntegerField(default=0)),
                (
                    "code",
                    models.CharField(blank=True, max_length=8, null=True, unique=True),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Net_Weight",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("Weight_type", models.CharField(default=None, max_length=50)),
                ("Weight_Price", models.IntegerField(default=0)),
                (
                    "Status",
                    models.CharField(
                        choices=[("1", "Active"), ("0", "Hide")],
                        default=1,
                        max_length=20,
                    ),
                ),
                ("created", models.DateTimeField(auto_now_add=True)),
                ("updated", models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name="taxes",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("tax_value", models.IntegerField(default=0)),
                ("tax_type", models.CharField(max_length=20)),
                (
                    "Status",
                    models.CharField(
                        choices=[("1", "Active"), ("0", "Hide")],
                        default=1,
                        max_length=20,
                    ),
                ),
                ("created", models.DateTimeField(auto_now_add=True)),
                ("updated", models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name="SubCategory",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=500)),
                (
                    "Status",
                    models.CharField(
                        choices=[("1", "Active"), ("0", "Hide")],
                        default=1,
                        max_length=20,
                    ),
                ),
                ("created", models.DateTimeField(auto_now_add=True)),
                ("updated", models.DateTimeField(auto_now=True)),
                (
                    "category",
                    models.ForeignKey(
                        default=1,
                        on_delete=django.db.models.deletion.CASCADE,
                        to="AdminPanel.category",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Stores",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("Store_Name", models.CharField(max_length=100)),
                ("Store_Address", models.CharField(max_length=1000)),
                (
                    "Store_Type",
                    models.CharField(
                        choices=[
                            ("brand", "Brand"),
                            ("cbd store", "CBD Store"),
                            ("dispensary", "Dispensary"),
                            ("delivery", "Delivery"),
                            ("doctor", "Doctor"),
                        ],
                        default=None,
                        max_length=50,
                    ),
                ),
                (
                    "Stores_Description",
                    ckeditor.fields.RichTextField(blank=True, default=None),
                ),
                (
                    "Store_Image",
                    models.ImageField(default=None, upload_to="media/Brand"),
                ),
                ("Stores_Website", models.URLField(blank=True, default=None)),
                (
                    "Stores_MobileNo",
                    phonenumber_field.modelfields.PhoneNumberField(
                        max_length=15, region=None, unique=True
                    ),
                ),
                (
                    "LicenceNo",
                    models.CharField(default=None, max_length=50, unique=True),
                ),
                (
                    "Status",
                    models.CharField(
                        choices=[("1", "Active"), ("0", "Hide")],
                        default=1,
                        max_length=20,
                    ),
                ),
                ("created", models.DateTimeField(auto_now_add=True)),
                ("updated", models.DateTimeField(auto_now=True)),
                (
                    "CityName",
                    models.ForeignKey(
                        default=1,
                        on_delete=django.db.models.deletion.CASCADE,
                        to="AdminPanel.cities",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="States",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("StateName", models.CharField(max_length=100)),
                (
                    "Status",
                    models.CharField(
                        choices=[("1", "Active"), ("0", "Hide")],
                        default=1,
                        max_length=20,
                    ),
                ),
                ("created", models.DateTimeField(auto_now_add=True)),
                ("updated", models.DateTimeField(auto_now=True)),
                (
                    "CountryName",
                    models.ForeignKey(
                        default=1,
                        on_delete=django.db.models.deletion.CASCADE,
                        to="AdminPanel.countries",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Product",
            fields=[
                ("id", models.AutoField(primary_key=True, serialize=False)),
                ("created", models.DateField(auto_now_add=True)),
                ("updated", models.DateField(auto_now=True)),
                ("Product_Name", models.CharField(max_length=100, unique=True)),
                ("Product_Details", models.CharField(default=None, max_length=150)),
                (
                    "SKU",
                    models.CharField(
                        blank=True, default=None, max_length=100, null=True
                    ),
                ),
                (
                    "Product_Image",
                    models.ImageField(default=None, upload_to="media/Products"),
                ),
                (
                    "Multiple_Image",
                    models.FileField(
                        default=None,
                        null=True,
                        upload_to="media/Products/MultipleImages",
                    ),
                ),
                (
                    "Product_Video",
                    models.FileField(null=True, upload_to="media/Videos"),
                ),
                ("quantity", models.IntegerField(default=1)),
                (
                    "strain",
                    models.CharField(
                        choices=[
                            ("N", "None"),
                            ("i", "Indica"),
                            ("s", "Sativa"),
                            ("h", "hybrid"),
                            ("c", "CBD"),
                        ],
                        default=None,
                        max_length=50,
                    ),
                ),
                (
                    "UPC",
                    models.CharField(
                        blank=True, default=None, max_length=100, null=True
                    ),
                ),
                ("prices", models.IntegerField(default=1)),
                ("Allow_tax", models.BooleanField(default=True)),
                ("Allow_discount", models.BooleanField(default=False)),
                ("Description", ckeditor.fields.RichTextField(default=None)),
                ("THC", models.IntegerField(blank=True, default=0)),
                ("CBD", models.IntegerField(blank=True, default=0)),
                ("CBN", models.IntegerField(blank=True, default=0)),
                (
                    "lab_Result",
                    models.CharField(
                        choices=[("percentage", "%"), ("Magnesium", "Mg")],
                        max_length=50,
                    ),
                ),
                ("tag", models.CharField(blank=True, default=None, max_length=50)),
                ("DiscountedAmount", models.IntegerField(blank=True, null=True)),
                ("taxedAmount", models.IntegerField(blank=True, null=True)),
                ("Alt_Text", models.CharField(default=None, max_length=50)),
                (
                    "Additional_Description",
                    ckeditor.fields.RichTextField(blank=True, default=None),
                ),
                ("Link", models.URLField(blank=True, default=None)),
                ("After_Coupoun_Price", models.IntegerField(blank=True, null=True)),
                (
                    "Stock",
                    models.CharField(
                        choices=[
                            ("In Stock", "IN STOCK"),
                            ("Out of Stock", "OUT OF STOCK"),
                        ],
                        default=1,
                        max_length=20,
                    ),
                ),
                (
                    "Status",
                    models.CharField(
                        choices=[("1", "Active"), ("0", "Hide")],
                        default=1,
                        max_length=20,
                    ),
                ),
                (
                    "After_GiftVoucher",
                    models.IntegerField(blank=True, default=None, null=True),
                ),
                ("SubTotal", models.IntegerField(blank=True, default=None, null=True)),
                (
                    "Brand",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        to="AdminPanel.brand",
                    ),
                ),
                (
                    "Claimed_Coupoun",
                    models.ForeignKey(
                        blank=True,
                        default=None,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        to="AdminPanel.claimedcoupon",
                    ),
                ),
                (
                    "GiftVoucher",
                    models.ForeignKey(
                        blank=True,
                        default=None,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        to="AdminPanel.claimgiftvoucher",
                    ),
                ),
                (
                    "Store",
                    models.ForeignKey(
                        default=1,
                        on_delete=django.db.models.deletion.CASCADE,
                        to="AdminPanel.stores",
                    ),
                ),
                (
                    "Sub_Category",
                    models.ForeignKey(
                        default=1,
                        on_delete=django.db.models.deletion.CASCADE,
                        to="AdminPanel.subcategory",
                    ),
                ),
                (
                    "discount",
                    models.ForeignKey(
                        blank=True,
                        default=0,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        to="AdminPanel.discount",
                    ),
                ),
                (
                    "flavour",
                    models.ForeignKey(
                        blank=True,
                        default=None,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        to="AdminPanel.flavours",
                    ),
                ),
                (
                    "net_weight",
                    models.ForeignKey(
                        default=None,
                        on_delete=django.db.models.deletion.CASCADE,
                        to="AdminPanel.net_weight",
                    ),
                ),
                (
                    "tax",
                    models.ForeignKey(
                        blank=True,
                        default=0,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        to="AdminPanel.taxes",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="News",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "StrainType",
                    models.CharField(
                        choices=[
                            ("N", "None"),
                            ("i", "Indica"),
                            ("s", "Sativa"),
                            ("h", "hybrid"),
                            ("c", "CBD"),
                        ],
                        default=None,
                        max_length=50,
                    ),
                ),
                ("Title", models.CharField(default=None, max_length=100)),
                ("Description", ckeditor.fields.RichTextField()),
                ("Image", models.ImageField(default=None, upload_to="media/Products")),
                ("Alt_Text", models.CharField(default=None, max_length=50)),
                ("Link", models.URLField(blank=True, default=None)),
                ("created", models.DateTimeField(auto_now_add=True)),
                ("updated", models.DateTimeField(auto_now=True)),
                (
                    "Category",
                    models.ForeignKey(
                        default=1,
                        on_delete=django.db.models.deletion.CASCADE,
                        to="AdminPanel.category",
                    ),
                ),
                (
                    "SubCategory",
                    models.ForeignKey(
                        blank=True,
                        default=None,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        to="AdminPanel.subcategory",
                    ),
                ),
            ],
        ),
        migrations.AddField(
            model_name="claimgiftvoucher",
            name="GiftVoucher",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, to="AdminPanel.giftvoucher"
            ),
        ),
        migrations.AddField(
            model_name="claimedcoupon",
            name="coupon",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, to="AdminPanel.coupon"
            ),
        ),
        migrations.AddField(
            model_name="cities",
            name="StatesName",
            field=models.ForeignKey(
                default=1,
                on_delete=django.db.models.deletion.CASCADE,
                to="AdminPanel.states",
            ),
        ),
    ]
