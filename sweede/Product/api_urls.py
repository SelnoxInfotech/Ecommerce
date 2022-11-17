from django.urls import path,include
from .views import *

urlpatterns = [
    path('Add-Category', AddCategories.as_view()),
    path('Get-Category', GetCategories.as_view()),
    path('update-Category/<int:id>', UpdateCategories.as_view()),
    path('delete-Category/<int:id>', DeleteCategory.as_view()),
    ###################################################################################################
    path('Add-SubCategory', AddSubCategories.as_view()),
    path('Get-SubCategory', GetSubCategories.as_view()),
    path('update-SubCategory/<int:id>', UpdateSubCategories.as_view()),
    path('delete-SubCategory/<int:id>', DeleteSubCategory.as_view()),
    ###################################################################################################
    # path('login/', MyObtainTokenPairView.as_view()),
    # path('Signup/', Signup.as_view()),
    ####################################################################################################
    path('Add-Country', AddCountry.as_view()),
    path('Get-Country', GetCountry.as_view()),
    path('update-Country/<int:id>', UpdateCountry.as_view()),
    path('delete-Country/<int:id>', DeleteCountry.as_view()),
    ####################################################################################################
    path('Add-States', AddStates.as_view()),
    path('Get-States', GetStates.as_view()),
    path('update-States/<int:id>', UpdateStates.as_view()),
    path('delete-States/<int:id>', DeleteStates.as_view()),
    ###################################################################################################
    path('Add-StrainType', AddStrainType.as_view()),
    path('Get-StrainType', GetStrainType.as_view()),
    path('update-StrainType/<int:id>', UpdateStrainType.as_view()),
    path('delete-StrainType/<int:id>', DeleteStrainType.as_view()),
    ###################################################################################################
    
    path('Add-Product', AddProduct.as_view()),
    path('Get-Product', GetProduct.as_view()),
    path('update-Product/<int:id>', UpdateProduct.as_view()),
    path('delete-Product/<int:id>', DeleteProduct.as_view()),
    #################################################################################################
    path('Add-Brand', AddBrand.as_view()),
    path('Get-Brand', GetBrand.as_view()),
    path('update-Brand/<int:id>', UpdateBrand.as_view()),
    path('delete-Brand/<int:id>', DeleteBrand.as_view()),
    ####################################################################################################
    path('Add-Tax', AddTax.as_view()),
    path('Get-Tax', GetTax.as_view()),
    path('update-Tax/<int:id>', UpdateTax.as_view()),
    path('delete-Tax/<int:id>', DeleteTax.as_view()),
    #####################################################################################################
    path('Add-Discount', AddDiscount.as_view()),
    path('Get-Discount', GetDiscount.as_view()),
    path('update-Discount/<int:id>', UpdateDiscount.as_view()),
    path('delete-Discount/<int:id>', DeleteDiscount.as_view()),
    #####################################################################################################


    
]