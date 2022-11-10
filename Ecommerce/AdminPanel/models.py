from django.db import models
import datetime
from .choices import *


# Create your models here.

class Category(models.Model):               #category table
    name=models.CharField(max_length=500)
    
   
    
class SubCategory(models.Model):            #Subcategory table
    name=models.CharField(max_length=500)
    category=models.ForeignKey(Category,on_delete=models.CASCADE,default=1)
    

class RegisterUser(models.Model):           #Signup
    Username=models.CharField(max_length=50)
    FirstName=models.CharField(max_length=50)
    LastName=models.CharField(max_length=50)
    Email=models.EmailField(max_length=100)
    Date_of_Birth=models.DateField(default=datetime.date.today)
    password=models.CharField(max_length=100)
    Gender=models.CharField(max_length=20)
    
    def register(self):
        self.save()
    @staticmethod
    def get_user_by_email(Email):
        try:
            return RegisterUser.objects.get(Email=Email)
        except:
            return False
    def isExists(self):
        if RegisterUser.objects.filter(Email=self.Email):
            return True
        return False
    
    
class Countries(models.Model):                      #Country Table
    CountryName=models.CharField(max_length=100)
    
    
class States(models.Model):                         #State Table
    StateName=models.CharField(max_length=100)
    CountryName=models.ForeignKey(Countries, on_delete=models.CASCADE,default=1)
    
    
class Cities(models.Model):                         #City Table
    CityName=models.CharField(max_length=100)
    StatesName=models.ForeignKey(States,on_delete=models.CASCADE,default=1)


class StrainType(models.Model):                        #Strain Types
    strain=models.CharField(max_length=50,choices=StrainTypes)
    

class LabResults(models.Model):                         #Lab result
    THC=models.IntegerField(default=1)
    CBD=models.IntegerField(default=1)
    CBN=models.IntegerField(default=1)
    
    
class Brand(models.Model):                  #Brand
    name=models.CharField(max_length=50,default=None)
    Brand_deiscription=models.CharField(max_length=500,default=None)
    Brand_Logo=models.ImageField(upload_to='media/Brand',default=None)
    


class Product(models.Model):                #Product
    Product_Name=models.CharField(max_length=100)    
    SKU=models.CharField(max_length=100)
    Category=models.ForeignKey(Category,on_delete=models.CASCADE,default=1)
    Sub_Category=models.ForeignKey(SubCategory,on_delete=models.CASCADE,default=1)
    UPC=models.CharField(max_length=100)
    Product_Image=models.ImageField(upload_to='media/Products',default=None)
    Strain_Types=models.ForeignKey(StrainType,on_delete=models.CASCADE,default=None)
    prices=models.IntegerField(default=1)
    lab_Result=models.ForeignKey(LabResults,on_delete=models.CASCADE,choices=LabResult)
    net_weight=models.CharField(max_length=50,choices=NetWeight,default=None)
    Product_Details=models.CharField(max_length=150,default=None)
    Brand=models.ForeignKey(Brand,on_delete=models.CASCADE,default=None)
    Description=models.CharField(max_length=500,default=None)
    tag=models.CharField(max_length=50,default=None)
    discount=models.IntegerField(default=None)
    Country=models.ForeignKey(Countries,on_delete=models.CASCADE,default=1)
    City=models.ForeignKey(Cities,on_delete=models.CASCADE,default=1)
    State=models.ForeignKey(States,on_delete=models.CASCADE,default=1)
