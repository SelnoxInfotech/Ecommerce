from django.contrib import admin
from .models import Category,SubCategory,Countries,States,Cities,Product,Brand,Stores,News,Discount,Net_Weight,Flavours,taxes,ExportFile
from .Coupoun import Coupon,ClaimedCoupon,GiftVoucher,ClaimGiftVoucher

# Register your models here.

admin.site.register(Category)
admin.site.register(SubCategory)
admin.site.register(Countries)
admin.site.register(States)
admin.site.register(Cities)
admin.site.register(Product)
admin.site.register(Brand)
admin.site.register(Stores)
admin.site.register(News)
admin.site.register(Coupon)
admin.site.register(ClaimedCoupon)
admin.site.register(Discount)
admin.site.register(Net_Weight)
admin.site.register(GiftVoucher)
admin.site.register(ClaimGiftVoucher)
admin.site.register(Flavours)
admin.site.register(taxes)
admin.site.register(ExportFile)







