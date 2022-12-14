from rest_framework import serializers
from .models import *
from django.contrib.auth.models import User
from rest_framework.validators import UniqueValidator
from django.contrib.auth.password_validation import validate_password
from import_export import resources



# from django.utils.encoding import force_text
from django.utils.encoding import force_str

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
        
        
class Serializer_Product(serializers.ModelSerializer):
    class Meta:
        model=Product
        fields='__all__'
        
   
        
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

     
        
        


class VerifyAccountSerializer(serializers.Serializer):
    email=serializers.EmailField()
    OTP=serializers.CharField()

# #Serializer to Get User Details using Django Token Authentication
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email')

# Register Serializer
class RegisterSerializer(serializers.ModelSerializer):


    class Meta:
        model=User
        fields=('id','username','email','password')
        extra_kwargs = {'password':{'write_only':True}}

    def create(self,validated_data):
        user=User.objects.create_superuser(validated_data['username'],validated_data['email'],validated_data['password'])

        return user
             
class Serializer_Store(serializers.ModelSerializer):
    class Meta:
      model=Stores
      fields='__all__'
        
    
class Serializer_News(serializers.ModelSerializer):
  class Meta:
    model=News
    fields='__all__'    
    
    
    
class Serializer_Net_Weight(serializers.ModelSerializer):
    class Meta:
        model=Net_Weight
        fields='__all__'
        
class Serializer_Flavour(serializers.ModelSerializer):
    class Meta:
        model=Flavours
        fields='__all__'
        
        
#################################################################################################################################################
################################################################TESTING##########################################################################
#################################################################################################################################################
from django.apps import apps
from django.utils.timezone import now

from .Coupoun import Coupon,ClaimedCoupon,GiftVoucher,ClaimGiftVoucher


class CouponSerializer(serializers.ModelSerializer):

    def validate(self, data):
        if 'expires' in data:
            if data['expires'] < now():
                raise serializers.ValidationError("Expiration date set in the past.")
        if data['type'] == 'percent':
            if 'value' in data and data['value'] > 1.0:
                raise serializers.ValidationError("Percentage discount specified greater than 100%.")

        if 'bound' in data and data['bound']:
            if 'user' not in data:
                raise serializers.ValidationError("Bound to user, but user field not specified.")

        qs = Coupon.objects.filter(code_l=data['code'].lower())
        if qs.count() > 0:
            if self.instance:
                if data['code'].lower() != self.instance.code_l:
                    raise serializers.ValidationError("Coupon code being updated to a code that already exists.")
            else:
                raise serializers.ValidationError("Creating coupon with code that violates uniqueness constraint.")

        data['code_l'] = data['code'].lower()

        return data

    def validate_repeat(self, value):

        if value < 0:
            raise serializers.ValidationError("Repeat field can be 0 for infinite, otherwise must be greater than 0.")

        return value

    def create(self, validated_data):
        return Coupon.objects.create(**validated_data)

    class Meta:
        model = apps.get_model('coupons.Coupon')
        fields = ('created', 'updated', 'code',
                  'code_l', 'type', 'expires',
                  'bound', 'user', 'repeat',
                  'value', 'id')


class ClaimedCouponSerializer(serializers.ModelSerializer):

    def validate(self, data):

        coupon = data['coupon']
        user = data['user']

        # Is the coupon expired?
        if coupon.expires and coupon.expires < now():
            raise serializers.ValidationError("Coupon has expired.")

        # Is the coupon bound to someone else?
        if coupon.bound and coupon.user.id != user.id:
            raise serializers.ValidationError("Coupon bound to another user.")

        # Is the coupon redeemed already beyond what's allowed?
        redeemed = ClaimedCoupon.objects.filter(coupon=coupon.id, user=user.id).count()
        if coupon.repeat > 0:
            if redeemed >= coupon.repeat:
                raise serializers.ValidationError("Coupon has been used to its limit.")

        return data

    class Meta:
        model = apps.get_model('coupons.ClaimedCoupon')
        fields = ('redeemed', 'coupon', 'user', 'id')
        

class GiftVoucherSerializer(serializers.ModelSerializer):

    def validate(self, data):
        if 'expires' in data:
            if data['expires'] < now():
                raise serializers.ValidationError("Expiration date set in the past.")
        if data['type'] == 'percent':
            if 'value' in data and data['value'] > 1.0:
                raise serializers.ValidationError("Percentage discount specified greater than 100%.")

        if 'bound' in data and data['bound']:
            if 'user' not in data:
                raise serializers.ValidationError("Bound to user, but user field not specified.")

        return data

    def validate_repeat(self, value):

        if value < 0:
            raise serializers.ValidationError("Repeat field can be 0 for infinite, otherwise must be greater than 0.")

        return value

    def create(self, validated_data):
        return GiftVoucher.objects.create(**validated_data)

    class Meta:
        model = GiftVoucher
        fields = '__all__'


class ClaimedGiftVoucherSerializer(serializers.ModelSerializer):

    def validate(self, data):

        GiftVoucher = data['GiftVoucher']
        user = data['user']

        # Is the coupon expired?
        if GiftVoucher.expires and GiftVoucher.expires < now():
            raise serializers.ValidationError("GiftVoucher has expired.")

        # Is the coupon bound to someone else?
        if GiftVoucher.bound and GiftVoucher.user.id != user.id:
            raise serializers.ValidationError("GiftVoucher bound to another user.")

        # Is the coupon redeemed already beyond what's allowed?
        redeemed = ClaimGiftVoucher.objects.filter(GiftVoucher=GiftVoucher.id, user=user.id).count()
        if GiftVoucher.repeat > 0:
            if redeemed >= GiftVoucher.repeat:
                raise serializers.ValidationError("GiftVoucher has been used to its limit.")

        return data

    class Meta:
        model = ClaimGiftVoucher
        fields = '__all__'
        

class ProductResource(resources.ModelResource):
    class Meta:
        model=Product
        fields='__all__'
        
