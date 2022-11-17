from django.contrib import admin
from .models import Category,SubCategory,Countries,States,Cities,StrainType,Product,Brand,taxes,Discount

# Register your models here.

admin.site.register(Category)
admin.site.register(SubCategory)
admin.site.register(Countries)
admin.site.register(States)
admin.site.register(Cities)
admin.site.register(StrainType)
admin.site.register(Product)
admin.site.register(Brand)
admin.site.register(taxes)
admin.site.register(Discount)



# admin.site.register(Discount)


