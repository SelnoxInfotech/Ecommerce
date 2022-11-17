from dataclasses import fields
from rest_framework import serializers
from .models import *



class Serializer_Category(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'
        

class Serializer_SubCategory(serializers.ModelSerializer):
    class Meta:
        model = SubCategory
        fields = '__all__'
        

class Serializer_Country(serializers.ModelSerializer):
    class Meta:
        model=Countries
        fields='__all__'
        
class Serializer_States(serializers.ModelSerializer):
    class Meta:
        model=States
        fields='__all__'
        
class Serializer_Cities(serializers.ModelSerializer):
    class Meta:
        model=Cities
        fields='__all__'
        
class Serializer_StrainType(serializers.ModelSerializer):
    class Meta:
        model=StrainType
        fields='__all__'
        

        
class Serializer_Product(serializers.ModelSerializer):
    class Meta:
        model=Product
        fields=('Product_Name','SKU','prices','discount')
        
class Serializer_Brand(serializers.ModelSerializer):
    class Meta:
        model=Brand
        fields='__all__'
        
class Serializer_tax(serializers.ModelSerializer):
    class Meta:
        model=taxes
        fields='__all__'
        
        
class Serializer_Discount(serializers.ModelSerializer):
    class Meta:
        models=Discount
        fields='__all__'

# class Serializer_Amount(serializers.ModelSerializer):
#     class Meta(object):
#         form= Amount
        
        
        
        
        
        
        
        
        
        