from django.db import models
import datetime
from .choices import *
import sys


# Create your models here.

class Category(models.Model):               #category table
    name=models.CharField(max_length=500)
    Status=models.CharField(max_length=20,default=1,choices=Status)
    
    
    
   
    
class SubCategory(models.Model):            #Subcategory table
    name=models.CharField(max_length=500)
    category=models.ForeignKey(Category,on_delete=models.CASCADE,default=1)
    Status=models.CharField(max_length=20,default=1,choices=Status)
    
    

    
class Countries(models.Model):                      #Country Table
    CountryName=models.CharField(max_length=100)
    Status=models.CharField(max_length=20,default=1,choices=Status)
    
    
    
class States(models.Model):                         #State Table
    StateName=models.CharField(max_length=100)
    CountryName=models.ForeignKey(Countries, on_delete=models.CASCADE,default=1)
    Status=models.CharField(max_length=20,default=1,choices=Status)
    
    
    
class Cities(models.Model):                         #City Table
    CityName=models.CharField(max_length=100)
    StatesName=models.ForeignKey(States,on_delete=models.CASCADE,default=1)
    Status=models.CharField(max_length=20,default=1,choices=Status)
    


class StrainType(models.Model):                        #Strain Types
    strain=models.CharField(max_length=50,choices=StrainTypes)
    Status=models.CharField(max_length=20,default=1,choices=Status)
    
    

class Brand(models.Model):                  #Brand
    name=models.CharField(max_length=50,default=None)
    Brand_deiscription=models.CharField(max_length=500,default=None)
    Brand_Logo=models.ImageField(upload_to='media/Brand',default=None)
    Status=models.CharField(max_length=20,default=1,choices=Status)
    
    
    
class taxes(models.Model):                    #tax
    tax_value=models.IntegerField(default=0)
    tax_type=models.CharField(max_length=20)
    Status=models.CharField(max_length=20,default=1,choices=Status)
    

class Discount(models.Model):                    #Discount
    Discount_value=models.IntegerField(default=0)
    Discount_type=models.CharField(max_length=20)   
    Status=models.CharField(max_length=20,default=1,choices=Status)
    



class Product(models.Model):                #Product
    id=models.AutoField(primary_key=True)
    Product_Name=models.CharField(max_length=100,unique=True)   
    Product_Details=models.CharField(max_length=150,default=None) 
    SKU=models.CharField(max_length=100)
    Category=models.ForeignKey(Category,on_delete=models.CASCADE,default=1)
    Sub_Category=models.ForeignKey(SubCategory,on_delete=models.CASCADE,default=1)
    Product_Image=models.ImageField(upload_to='media/Products',default=None)
    Multiple_Image=models.FileField(upload_to='media/Products/MultipleImages',default=None,null=True)
    Product_Video = models.FileField(upload_to="media/Videos",null= True)
    quantity=models.IntegerField(default=1)
    Strain_Types=models.ForeignKey(StrainType,on_delete=models.CASCADE,default=None)
    UPC=models.CharField(max_length=100)
    prices=models.IntegerField(default=1,blank=True,null=True)
    AlloW_tax=models.BooleanField(default=True)
    tax=models.ForeignKey(taxes,on_delete=models.CASCADE,default=1,blank=True,null=True)
    Allow_discount=models.BooleanField(default=False)
    discount=models.ForeignKey(Discount,on_delete=models.CASCADE,default=1,blank=True,null=True)
    net_weight=models.CharField(max_length=50,choices=NetWeight,default=None)
    Brand=models.ForeignKey(Brand,on_delete=models.CASCADE,blank=True,null=True)
    Description=models.CharField(max_length=500,default=None)
    THC=models.IntegerField(default=0,blank=True)
    CBD=models.IntegerField(default=0,blank=True)
    CBN=models.IntegerField(default=0,blank=True)
    lab_Result=models.CharField(max_length=50,choices=LabResult)
    tag=models.CharField(max_length=50,default=None,blank=True)
    Country=models.ForeignKey(Countries,on_delete=models.CASCADE,default=1)
    City=models.ForeignKey(Cities,on_delete=models.CASCADE,default=1)
    State=models.ForeignKey(States,on_delete=models.CASCADE,default=1)
    Stock=models.CharField(max_length=20,default=1,choices=Check_Stock)
    Status=models.CharField(max_length=20,default=1,choices=Status)
    DiscountedAmount=models.IntegerField(blank=True,null=True)
    taxedAmount=models.IntegerField(blank=True,null=True)
    Alt_Text=models.CharField(max_length=50,default=None,blank=False)
    
    def save(self,*args,**kwargs):
        if self.discount.Discount_value>0:
            self.DiscountedAmount=self.prices-(self.prices * self.discount.Discount_value)/100
        else:
            raise
        if self.discount.Discount_value>0<self.tax.tax_value :
            self.taxedAmount=self.DiscountedAmount-(self.DiscountedAmount * self.tax.tax_value)/100
        else :
            self.taxedAmount=self.prices-(self.prices*self.tax.tax_value)/100
        
        self.prices=self.prices*self.quantity
        super().save(*args,**kwargs) 
        
    

