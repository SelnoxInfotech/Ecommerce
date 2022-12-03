from django.db import models
from .models import *
from django.conf import settings
import secrets


COUPON_TYPES = (
    ('percent', 'percent'),
    ('value', 'value'),
)


try:
    user = settings.AUTH_USER_MODEL
except AttributeError:
    from django.contrib.auth.models import User
    

class Coupon(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    code = models.CharField(max_length=64)
    code_l = models.CharField(max_length=64, blank=True, unique=True)
    type = models.CharField(max_length=16, choices=COUPON_TYPES)
    expires = models.DateTimeField(blank=True, null=True)
    percentage = models.DecimalField(default=1.0, max_digits=5, decimal_places=2)
    bound = models.BooleanField(default=False)
    # user = models.ForeignKey(User,on_delete=models.DO_NOTHING)
    repeat = models.IntegerField(default=0)
    def __str__(self):
        return self.code
    


class ClaimedCoupon(models.Model):
    redeemed = models.DateTimeField(auto_now_add=True)
    coupon = models.ForeignKey(Coupon,on_delete=models.CASCADE)
    # user = models.ForeignKey(user,on_delete=models.CASCADE)  
    def __str__(self):
        return self.coupon.code
    
    
    
class GiftVoucher(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    type = models.CharField(max_length=16, choices=COUPON_TYPES)
    expires = models.DateTimeField(blank=True, null=True)
    percentage = models.DecimalField(default=0.0, max_digits=5, decimal_places=2)
    bound = models.BooleanField(default=False)
    # user = models.ForeignKey(User,on_delete=models.DO_NOTHING)
    repeat = models.IntegerField(default=0)
    code = models.CharField(max_length=8, blank=True, null=True, unique=True)
    def save(self,*args,**kwargs):
        if self.percentage!=0:
            upper_alpha = "ABCDEFGHIJKLMNOPQRSTVWXYZabcdefghijklmnopqrstuvwxyz1234567890"
            random_str = "".join(secrets.choice(upper_alpha) for i in range(8))
            self.code = (random_str)[-8:]
        super().save(*args,**kwargs) 

    def __str__(self):
        return self.code
    

class ClaimGiftVoucher(models.Model):
    redeemed = models.DateTimeField(auto_now_add=True)
    GiftVoucher = models.ForeignKey(GiftVoucher,on_delete=models.CASCADE)
    # user = models.ForeignKey(user,on_delete=models.CASCADE)   
    def __str__(self):
        return self.GiftVoucher.code
    
    
    





