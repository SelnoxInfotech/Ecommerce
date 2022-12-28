from django.urls import path
from .views import *
from .serializer import *
from rest_framework import routers
from knox import views as knox_views
from . import views
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)



router=routers.SimpleRouter()
router.register(r'ProductViewSet/',views.ProductViewSet,basename="ProductViewSet")
router.register(r'MultipleImageUpload/',views.MultipleImageUpload,basename="MultipleImageUpload")
router.register(r'Adding_Multiple_Store/',views.Adding_Multiple_Store,basename="Adding_Multiple_Store")
router.register(r'coupon/', CouponViewSet,basename='Coupon')
router.register(r'redeemedCoupon/', ClaimedCouponViewSet,basename='RedeemedCoupon')
router.register(r'GiftVoucher/', GiftVoucherViewSet,basename='GiftVoucher')
router.register(r'redeemedGiftVoucher/', ClaimGiftVoucherViewSet,basename='RedeemedGiftVoucher')



urlpatterns = [
    path('Add-Category/', AddCategories.as_view()),
    path('Get-Category/', GetCategories.as_view()),
    path('update-Category/<int:id>', UpdateCategories.as_view()),
    path('delete-Category/<int:id>', DeleteCategory.as_view()),
    ###################################################################################################
    path('Add-SubCategory/', AddSubCategories.as_view()),
    path('Get-SubCategory/', GetSubCategories.as_view()),
    
    path('update-SubCategory/<int:id>', UpdateSubCategories.as_view()),
    path('delete-SubCategory/<int:id>', DeleteSubCategory.as_view()),
    ###################################################################################################
    path("Login/",LoginAPI.as_view()),
    path("get-UserAPI/",UserAPI.as_view()),
    path('register/',RegisterAPI.as_view()),
    path('VerifyOtp/',VerifyOtpLogin.as_view()),
    path('logout/',knox_views.LogoutView.as_view(),name='logout'),
    path('ResetPasswordAPI/',ResetPasswordAPI.as_view(),name='ResetPasswordAPI'),
    path('VerifyOtpResetPassword/',VerifyOtpResetPassword.as_view(),name='VerifyOtpResetPassword'),
    path('logoutall/',knox_views.LogoutAllView.as_view(),name='logoutall'),
    ########################################################################################################
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('token/verify/', TokenVerifyView.as_view(), name='token_verify'),
    ####################################################################################################
    path('Add-Country/', AddCountry.as_view()),
    path('Get-Country/', GetCountry.as_view()),
    path('update-Country/<int:id>', UpdateCountry.as_view()),
    path('delete-Country/<int:id>', DeleteCountry.as_view()),
    ####################################################################################################
    path('Add-States/', AddStates.as_view()),
    path('Get-States/', GetStates.as_view()),
    path('update-States/<int:id>', UpdateStates.as_view()),
    path('delete-States/<int:id>', DeleteStates.as_view()),
    ###################################################################################################
    path('Add-Product/', AddProduct.as_view()),
    path('Get-Product/', GetProduct.as_view()),
    path('update-Product/<int:id>', UpdateProduct.as_view()),
    path('delete-Product/<int:id>', DeleteProduct.as_view()),
    #################################################################################################
    path('Add-Brand/', AddBrand.as_view()),
    path('Get-Brand/', GetBrand.as_view()),
    path('update-Brand/<int:id>', UpdateBrand.as_view()),
    path('delete-Brand/<int:id>', DeleteBrand.as_view()),
    ####################################################################################################
    path('Add-Tax/', AddTax.as_view()),
    path('Get-Tax/', GetTax.as_view()),
    path('update-Tax/<int:id>', UpdateTax.as_view()),
    path('delete-Tax/<int:id>', DeleteTax.as_view()),
    #####################################################################################################
    path('Add-Discount/', AddDiscount.as_view()),
    path('Get-Discount/', GetDiscount.as_view()),
    path('update-Discount/<int:id>', UpdateDiscount.as_view()),
    path('delete-Discount/<int:id>', DeleteDiscount.as_view()),
    #####################################################################################################
    path('Add-News/', AddNews.as_view()),
    path('Get-News/', GetNews.as_view()),
    path('update-News/<int:id>', UpdateNews.as_view()),
    path('delete-News/<int:id>', DeleteNews.as_view()),
    #####################################################################################################
    path('Add-NetWeight/', AddNet_Weight.as_view()),
    path('Get-NetWeight/', GetNet_Weight.as_view()),
    path('update-NetWeight/<int:id>', UpdateNet_Weight.as_view()),
    path('delete-NetWeight/<int:id>', DeleteNet_Weight.as_view()),
    #####################################################################################################
    path('Add-Flavours/', AddFlavours.as_view()),
    path('Get-Flavours/', GetFlavours.as_view()),
    path('update-Flavours/<int:id>', UpdateFlavours.as_view()),
    path('delete-Flavours/<int:id>', DeleteFlavours.as_view()),
    #####################################################################################################
    path('Add-Cities/', AddCities.as_view()),
    path('Get-Cities/', GetCities.as_view()),
    path('update-Cities/<int:id>', UpdateCities.as_view()),
    path('delete-Cities/<int:id>', DeleteCities.as_view()),
    #####################################################################################################
    path('Add-Stores/', AddStores.as_view()),
    path('Get-Stores/', GetStores.as_view()),
    path('update-Stores/<int:id>', UpdateStores.as_view()),
    path('delete-Stores/<int:id>', DeleteStores.as_view()),
    #####################################################################################################
    path('Replicate-data/<int:id>', Replicate_data.as_view(),name="Replicate Data"),
    path('ExportImportExcel/', ExportImportExcel.as_view(),name="ExportImportExcel"),
    path('Get_Deal/', Get_Deal.as_view(queryset=Product.objects.all(), serializer_class=Serializer_Product), name='Get_Deal'),
    #########################################################################################################################
    path('Get-CountCategories/', GetCountCategories.as_view()),
    path('Get-CountBrand/', GetCountBrand.as_view()),
    path('Get-CountProduct/', GetCountProduct.as_view()),
    path('Get-CountStore/', GetCountStore.as_view()),
    path('Get-CountNews/', GetCountNews.as_view()),
    path('Get-TotalCount/', TotalCount.as_view()),
    
    path('Get-CountSubCategories/', GetCountSubCategories.as_view()),
    #############################################################################################################################
    path('Get-TotalProductGraph/', TotalProductGraph.as_view()),
    path('Get-Test/', Test.as_view()),
    
    
    
]+router.urls


