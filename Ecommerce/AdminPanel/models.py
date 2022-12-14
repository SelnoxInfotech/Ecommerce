from django.db import models
import datetime
from .choices import *
import sys
from ckeditor.fields import RichTextField
from phonenumber_field.modelfields import PhoneNumberField
from .Coupoun import ClaimedCoupon,ClaimGiftVoucher


# Create your models here.

class Category(models.Model):               #category table
    name=models.CharField(max_length=500)
    Status=models.CharField(max_length=20,default=1,choices=Status)
    
    def __str__(self):
        return self.name
    
    
    
   
    
class SubCategory(models.Model):            #Subcategory table
    name=models.CharField(max_length=500)
    category=models.ForeignKey(Category,on_delete=models.CASCADE,default=1)
    Status=models.CharField(max_length=20,default=1,choices=Status)
    
    def __str__(self):
        return self.name

    
class Countries(models.Model):                      #Country Table
    CountryName=models.CharField(max_length=100)
    Status=models.CharField(max_length=20,default=1,choices=Status)
    def __str__(self):
        return self.CountryName
    
    
class States(models.Model):                         #State Table
    StateName=models.CharField(max_length=100)
    CountryName=models.ForeignKey(Countries, on_delete=models.CASCADE,default=1)
    Status=models.CharField(max_length=20,default=1,choices=Status)
    
    def __str__(self):
        return self.StateName
    
class Cities(models.Model):                         #City Table
    CityName=models.CharField(max_length=100)
    StatesName=models.ForeignKey(States,on_delete=models.CASCADE,default=1)
    Status=models.CharField(max_length=20,default=1,choices=Status)
    def __str__(self):
        return self.CityName
    

class Stores(models.Model):
    CityName=models.ForeignKey(Cities,on_delete=models.CASCADE,default=1)
    Store_Name=models.CharField(max_length=100)
    Store_Address=models.CharField(max_length=1000)
    Stores_Description=RichTextField(default=None,blank=True)
    Store_Image=models.ImageField(upload_to='media/Brand',default=None)
    Stores_Website=models.URLField(max_length=200,blank=True,default=None)
    Stores_MobileNo=PhoneNumberField(unique = True, null = False, blank = False,max_length=15)
    LicenceNo=models.CharField(max_length=50,default=None,unique=True)
    Status=models.CharField(max_length=20,default=1,choices=Status)
    
    
    def __str__(self):
        return self.Store_Name
    

class Brand(models.Model):                  #Brand
    name=models.CharField(max_length=50,default=None)
    Brand_description=RichTextField(default=None)
    Brand_Logo=models.ImageField(upload_to='media/Brand',default=None)
    Status=models.CharField(max_length=20,default=1,choices=Status)
    Link=models.URLField(max_length=200,blank=True,default=None)
    def __str__(self):
        return self.name
    
    
    
    
class taxes(models.Model):                    #tax
    tax_value=models.IntegerField(default=0)
    tax_type=models.CharField(max_length=20)
    Status=models.CharField(max_length=20,default=1,choices=Status)
    def __str__(self):
        return self.tax_type
    

class Discount(models.Model):                    #Discount
    Discount_value=models.IntegerField(default=0)
    Discount_type=models.CharField(max_length=20)   
    Status=models.CharField(max_length=20,default=1,choices=Status)
    def __str__(self):
        return self.Discount_type
    
class Flavours(models.Model):                   #Flavour
    flavour_Name=models.CharField(max_length=50,default=None)
    Price=models.IntegerField(default=0)
    FlavoursImage=models.ImageField(upload_to='media/Products',default=None)
    
    def __str__(self):
        return self.flavour_Name
    

class Net_Weight(models.Model):                 #Net Weight
    Weight_type=models.CharField(max_length=50,default=None)
    Weight_Price=models.IntegerField(default=0)
    Status=models.CharField(max_length=20,default=1,choices=Status)
    
    def __str__(self):
        return self.Weight_type
    

class Product(models.Model):                #Product
    id=models.AutoField(primary_key=True)
    Product_Name=models.CharField(max_length=100,unique=True)   
    Product_Details=models.CharField(max_length=150,default=None) 
    SKU=models.CharField(max_length=100,default=None,blank=True,null=True)
    Sub_Category=models.ForeignKey(SubCategory,on_delete=models.CASCADE,default=1)
    Product_Image=models.ImageField(upload_to='media/Products',default=None)
    Multiple_Image=models.FileField(upload_to='media/Products/MultipleImages',default=None,null=True)
    Product_Video = models.FileField(upload_to="media/Videos",null= True)
    quantity=models.IntegerField(default=1)
    strain=models.CharField(max_length=50,choices=StrainTypes,default=None)
    UPC=models.CharField(max_length=100,blank=True,null=True,default=None)
    prices=models.IntegerField(default=1)
    Allow_tax=models.BooleanField(default=True)
    tax=models.ForeignKey(taxes,on_delete=models.CASCADE,blank=True,default=0,null=True)
    Allow_discount=models.BooleanField(default=False)
    discount=models.ForeignKey(Discount,on_delete=models.CASCADE,blank=True,default=0,null=True)
    net_weight=models.ForeignKey(Net_Weight,on_delete=models.CASCADE,default=None)
    Brand=models.ForeignKey(Brand,on_delete=models.CASCADE,blank=True,null=True)
    Description=RichTextField(default=None)
    THC=models.IntegerField(default=0,blank=True)
    CBD=models.IntegerField(default=0,blank=True)
    CBN=models.IntegerField(default=0,blank=True)
    lab_Result=models.CharField(max_length=50,choices=LabResult)
    tag=models.CharField(max_length=50,default=None,blank=True)
    Store=models.ForeignKey(Stores,on_delete=models.CASCADE,default=1)
    flavour=models.ForeignKey(Flavours,on_delete=models.CASCADE,default=None,blank=True,null=True)
    DiscountedAmount=models.IntegerField(blank=True,null=True)
    taxedAmount=models.IntegerField(blank=True,null=True)
    Alt_Text=models.CharField(max_length=50,default=None,blank=False)
    Additional_Description=RichTextField(blank=True,default=None)
    Link=models.URLField(max_length=200,blank=True,default=None)
    Claimed_Coupoun=models.ForeignKey(ClaimedCoupon,on_delete=models.CASCADE,blank=True,default=None,null=True)
    After_Coupoun_Price=models.IntegerField(blank=True,null=True)
    Stock=models.CharField(max_length=20,default=1,choices=Check_Stock) 
    Status=models.CharField(max_length=20,default=1,choices=Status)
    GiftVoucher=models.ForeignKey(ClaimGiftVoucher,on_delete=models.CASCADE,blank=True,default=None,null=True)
    After_GiftVoucher=models.IntegerField(blank=True,null=True,default=None)
    
    
    
    
    def save(self,*args,**kwargs):
        if self.discount.Discount_value>0:
            self.DiscountedAmount=self.prices-(self.prices * self.discount.Discount_value)/100
        else:
            self.DiscountedAmount=self.prices
        if  self.tax.tax_value>0:
            self.taxedAmount=self.DiscountedAmount-(self.DiscountedAmount * self.tax.tax_value)/100
        elif self.tax.tax_value==0 or self.tax.tax_value==None:
            self.taxedAmount=self.DiscountedAmount
            
        elif self.tax !=0  :
            self.taxedAmount=self.prices-(self.prices*self.tax.tax_value)/100
        else:
            self.taxedAmount=self.prices
        if self.prices>5 and self.DiscountedAmount!=0:
            self.After_Coupoun_Price=self.DiscountedAmount-(self.DiscountedAmount*float(self.Claimed_Coupoun.coupon.percentage))/100
        elif self.prices>5 and self.taxedAmount!=0:
            self.After_Coupoun_Price=self.taxedAmount-(self.taxedAmount*self.Claimed_Coupoun.coupon.percentage)/100
        elif self.prices>5 and self.DiscountedAmount==0 and self.taxedAmount==0:
            self.After_Coupoun_Price=self.prices-(self.prices*self.Claimed_Coupoun.coupon.percentage)/100
        else:
            raise("Price Amount must be more then 5")
        if self.Claimed_Coupoun.coupon.percentage==0 or self.Claimed_Coupoun.coupon.percentage==None:
            self.After_GiftVoucher=self.taxedAmount-(self.GiftVoucher.GiftVoucher.percentage * self.taxedAmount)/100
        
                
        super().save(*args,**kwargs) 
    def __str__(self):
        return self.Product_Name
        
    


class News(models.Model):
    Category=models.ForeignKey(Category,on_delete=models.CASCADE,default=1)
    SubCategory=models.ForeignKey(SubCategory,on_delete=models.CASCADE,blank=True,default=None,null=True)
    StrainType=models.CharField(max_length=50,choices=StrainTypes,default=None)
    Title=models.CharField(max_length=100,default=None)
    Description=RichTextField()
    Image=models.ImageField(upload_to='media/Products',default=None)
    Alt_Text=models.CharField(max_length=50,default=None,blank=False)
    Link=models.URLField(max_length=200,blank=True,default=None)



class ExportFile(models.Model):
    File=models.FileField(upload_to="excel")
    
    
###########################################################################################################################################
from django.db import models

# Create your models here.
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token

@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)
