from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework import generics
from .models import Category,SubCategory,Countries,States,Cities,Brand,Product,taxes,Discount,Stores,News,Net_Weight,Flavours
from .serializer import Serializer_Category,Serializer_SubCategory,Serializer_Country,Serializer_States,Serializer_Cities,Serializer_Product,Serializer_Brand,Serializer_tax,Serializer_Discount
from django.shortcuts import get_object_or_404
from rest_framework.viewsets import ModelViewSet  
from rest_framework import viewsets
from rest_framework.parsers import MultiPartParser,FormParser
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter, SearchFilter

from .serializer import UserSerializer,RegisterSerializer,Serializer_Store,Serializer_News,Serializer_Net_Weight,Serializer_Flavour,GiftVoucherSerializer,ClaimedGiftVoucherSerializer
from rest_framework import generics, permissions
from rest_framework.response import Response
from knox.models import AuthToken
from .serializer import UserSerializer,  RegisterSerializer,VerifyAccountSerializer
from django.contrib.auth import login
from django.contrib.auth.models import User

from rest_framework.authtoken.serializers import AuthTokenSerializer
from knox.views import LoginView as KnoxLoginView

from Ecommerce.settings import EMAIL_BACKEND,EMAIL_HOST,EMAIL_HOST_USER,EMAIL_HOST_PASSWORD,EMAIL_PORT,EMAIL_USE_TLS,DEFAULT_FROM_EMAIL 
import smtplib
import random
Otp=random.randint(1000, 9999)
# Class based view to Get User Details using Token Authentication
def send_OneToOneMail(from_email='',to_emails=''):
    server=smtplib.SMTP(EMAIL_HOST,EMAIL_PORT)
    server.ehlo()
    server.starttls()
    server.login(EMAIL_HOST_USER,EMAIL_HOST_PASSWORD)
    Subject="Selnox"
    Text="Your One Time Password is "  + str(Otp)
    
    msg='Subject: {}\n\n{}'.format(Subject, Text)
    server.sendmail(from_email,to_emails,msg)
    user=User.objects.get(email=to_emails)
    user.otp=Otp
    user.save()
    server.quit()
    
class VerifyOtp(APIView):
    def post(self,request):
        data=request.data
        serializer=VerifyAccountSerializer(data=data)
        serializer.is_valid()
        email=serializer.data['email']
        send_OneToOneMail(from_email='smtpselnox@gmail.com',to_emails=email)
        otp=serializer.data['OTP']
        
        user=User.objects.filter(email=email)
        if not user.exists():
            return Response({
                'message':'Something goes wrong',
                'data':'invalid Email'
            })
        if user[0].otp != otp:
            return Response({
                'message':'Something goes wrong',
                'data':'invalid Otp'
            })
        user=user.first()
        user.is_verified=True
        user.save()
        return Response({
                'message':'User is Verified',
                'data':{}
            })
    
    
    
    
class LoginAPI(KnoxLoginView):
    permission_classes=(permissions.AllowAny,)


    def post(self,request,format=None):
        serializer=AuthTokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user=serializer.validated_data['user']
        email=serializer.validated_data['email']
        otp=serializer.validated_data['OTP']
        
        user=User.objects.filter(email=email)
        if not user.exists():
            return Response({
                'message':'Something goes wrong',
                'data':'invalid Email'
            })
        if user[0].otp != otp:
            return Response({
                'message':'Something goes wrong',
                'data':'invalid Otp'
            })
        user=user.first()
         
        login(request,user)
        return super(LoginAPI,self).post(request,format=None)

#Class based view to register user
class RegisterAPI(generics.GenericAPIView):
    serializer_class =RegisterSerializer

    def post(self,request,*args,**kwargs):
        serializer=self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user=serializer.save()
        email=serializer.validated_data['email']
        
        return Response({
        "user":UserSerializer(user,context=self.get_serializer_context()).data,
        "token":AuthToken.objects.create(user)[1]
        })
#Category Api
class GetCategories(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        User = Category.objects.select_related().all()
        serialize = Serializer_Category(User, many=True)
        
        return Response(serialize.data)
    
class AddCategories(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = Serializer_Category(data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({"status": "success","data": serializer.data}, status=status.HTTP_201_CREATED)
        else:
            return Response({"status": "error", "data": serializer.errors})

class UpdateCategories(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, id=None):
        User = Category.objects.get(id=id)
        serializer = Serializer_Category(User, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save(modified_by=request.user.username)
            return Response({"status": "success", "data": serializer.data}, status=status.HTTP_200_OK)
        else:
            return Response({"status": "error", "data": serializer.errors})

class DeleteCategory(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request, id=None):
        User = get_object_or_404(Category, id=id)
        User.delete()
        return Response({"status": "success", "data": "Deleted"})
 
 
#Sub Category Api
class GetSubCategories(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        User = SubCategory.objects.select_related().all()
        serialize = Serializer_SubCategory(User, many=True)
        return Response(serialize.data)

class AddSubCategories(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = Serializer_SubCategory(data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({"status": "success","data": serializer.data}, status=status.HTTP_201_CREATED)
        else:
            return Response({"status": "error", "data": serializer.errors})


class UpdateSubCategories(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, id=None):
        User = SubCategory.objects.get(id=id)
        serializer = Serializer_SubCategory(User, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save(modified_by=request.user.username)
            return Response({"status": "success", "data": serializer.data}, status=status.HTTP_200_OK)
        else:
            return Response({"status": "error", "data": serializer.errors})


class DeleteSubCategory(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request, id=None):
        User = get_object_or_404(SubCategory, id=id)
        User.delete()
        return Response({"status": "success", "data": "Deleted"})



#Country
class GetCountry(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        User = Countries.objects.select_related().all()
        serialize = Serializer_Country(User, many=True)
        
        return Response(serialize.data)
    
class AddCountry(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = Serializer_Country(data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({"status": "success","data": serializer.data}, status=status.HTTP_201_CREATED)
        else:
            return Response({"status": "error", "data": serializer.errors})


class UpdateCountry(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, id=None):
        User = Countries.objects.get(id=id)
        serializer = Serializer_Country(User, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save(modified_by=request.user.username)
            return Response({"status": "success", "data": serializer.data}, status=status.HTTP_200_OK)
        else:
            return Response({"status": "error", "data": serializer.errors})


class DeleteCountry(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request, id=None):
        User = get_object_or_404(Countries, id=id)
        User.delete()
        return Response({"status": "success", "data": "Deleted"})
    
    
#States
class GetStates(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        User = States.objects.select_related().all()
        serialize = Serializer_States(User, many=True)
        
        return Response(serialize.data)
    
class AddStates(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = Serializer_States(data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({"status": "success","data": serializer.data}, status=status.HTTP_201_CREATED)
        else:
            return Response({"status": "error", "data": serializer.errors})


class UpdateStates(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, id=None):
        User = States.objects.get(id=id)
        serializer = Serializer_States(User, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save(modified_by=request.user.username)
            return Response({"status": "success", "data": serializer.data}, status=status.HTTP_200_OK)
        else:
            return Response({"status": "error", "data": serializer.errors})


class DeleteStates(APIView):
    permission_classes = [IsAuthenticated]
    def delete(self, request, id=None):
        User = get_object_or_404(States, id=id)
        User.delete()
        return Response({"status": "success", "data": "Deleted"})
    
    
#Cities 
class GetCities(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        User = Cities.objects.select_related().all()
        serialize = Serializer_Cities(User, many=True)
        
        return Response(serialize.data)
    
class AddCities(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = Serializer_Cities(data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({"status": "success","data": serializer.data}, status=status.HTTP_201_CREATED)
        else:
            return Response({"status": "error", "data": serializer.errors})


class UpdateCities(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, id=None):
        User = Cities.objects.get(id=id)
        serializer = Serializer_Cities(User, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save(modified_by=request.user.username)
            return Response({"status": "success", "data": serializer.data}, status=status.HTTP_200_OK)
        else:
            return Response({"status": "error", "data": serializer.errors})


class DeleteCities(APIView):
    permission_classes = [IsAuthenticated]
    def delete(self, request, id=None):
        User = get_object_or_404(Cities, id=id)
        User.delete()
        return Response({"status": "success", "data": "Deleted"})
        
        
#Product
class GetProduct(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        User = Product.objects.select_related().all()
        serialize = Serializer_Product(User, many=True)
        
        return Response(serialize.data)

class AddProduct(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = Serializer_Product(data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({"status": "success","data": serializer.data}, status=status.HTTP_201_CREATED)
        else:
            return Response({"status": "error", "data": serializer.errors})
    

class UpdateProduct(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, id=None):
        User = Product.objects.get(id=id)
        serializer = Serializer_Product(User, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save(modified_by=request.user.username)
            return Response({"status": "success", "data": serializer.data}, status=status.HTTP_200_OK)
        else:
            return Response({"status": "error", "data": serializer.errors})


class DeleteProduct(APIView):
    permission_classes = [IsAuthenticated]
    def delete(self, request, id=None):
        User = get_object_or_404(Product, id=id)
        User.delete()
        return Response({"status": "success", "data": "Deleted"})
        
        
#Brand
class GetBrand(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        User = Brand.objects.select_related().all()
        serialize = Serializer_Brand(User, many=True)
        
        return Response(serialize.data)
    
class AddBrand(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = Serializer_Brand(data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({"status": "success","data": serializer.data}, status=status.HTTP_201_CREATED)
        else:
            return Response({"status": "error", "data": serializer.errors})


class UpdateBrand(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, id=None):
        User = Brand.objects.get(id=id)
        serializer = Serializer_Brand(User, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save(modified_by=request.user.username)
            return Response({"status": "success", "data": serializer.data}, status=status.HTTP_200_OK)
        else:
            return Response({"status": "error", "data": serializer.errors})


class DeleteBrand(APIView): 
    permission_classes = [IsAuthenticated]
    def delete(self, request, id=None):
        User = get_object_or_404(Brand, id=id)
        User.delete()
        return Response({"status": "success", "data": "Deleted"})
        

#tax
class GetTax(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        User = taxes.objects.select_related().all()
        serialize = Serializer_tax(User, many=True)
        return Response(serialize.data)
    
class AddTax(APIView): 
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = Serializer_tax(data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({"status": "success","data": serializer.data}, status=status.HTTP_201_CREATED)
        else:
            return Response({"status": "error", "data": serializer.errors})


class UpdateTax(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, id=None):
        User = taxes.objects.get(id=id)
        serializer = Serializer_tax(User, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save(modified_by=request.user.username)
            return Response({"status": "success", "data": serializer.data}, status=status.HTTP_200_OK)
        else:
            return Response({"status": "error", "data": serializer.errors})


class DeleteTax(APIView): 
    permission_classes = [IsAuthenticated]
    
    def delete(self, request, id=None):
        User = get_object_or_404(taxes, id=id)
        User.delete()
        return Response({"status": "success", "data": "Deleted"})
    



#Discount
class GetDiscount(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        User = Discount.objects.select_related().all()
        serialize = Serializer_Discount(User, many=True)
        return Response(serialize.data)
    
class AddDiscount(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = Serializer_Discount(data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({"status": "success","data": serializer.data}, status=status.HTTP_201_CREATED)
        else:
            return Response({"status": "error", "data": serializer.errors})


class UpdateDiscount(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, id=None):
        User = Discount.objects.get(id=id)
        serializer = Serializer_Discount(User, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save(modified_by=request.user.username)
            return Response({"status": "success", "data": serializer.data}, status=status.HTTP_200_OK)
        else:
            return Response({"status": "error", "data": serializer.errors})


class DeleteDiscount(APIView): 
    permission_classes = [IsAuthenticated]
    
    def delete(self, request, id=None):
        User = get_object_or_404(Discount, id=id)
        User.delete()
        return Response({"status": "success", "data": "Deleted"})


     
#Replicate or Duplicate Data
class Replicate_data(APIView):
    def post(self, request, id=None):
        User = Product.objects.get(id=id)
        serializer = Serializer_Product(User, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({"status": "success", "data": serializer.data}, status=status.HTTP_200_OK)
        else:
            return Response({"status": "error", "data": serializer.errors})
        
        
        
# Adding Multiple Images
def modify_input_for_multiple_files(image):
    dict = {}
    dict['Multiple_Image'] = image
    return dict

class MultipleImageUpload(viewsets.ModelViewSet):
    queryset=Product.objects.all()
    serializer_class=Serializer_Product
    def post(self, request, *args, **kwargs):
        parser_classes = (MultiPartParser, FormParser)

        # converts querydict to original dict
        images = dict((request.data).lists())['Multiple_Image']
        flag = 1
        arr = []
        for img_name in images:
            modified_data = modify_input_for_multiple_files(img_name)
            file_serializer = Serializer_Product(data=modified_data)
            if file_serializer.is_valid():
                file_serializer.save()
                arr.append(file_serializer.data)
            else:
                flag = 0

        if flag == 1:
            return Response(arr, status=status.HTTP_201_CREATED)
        else:
            return Response(arr, status=status.HTTP_400_BAD_REQUEST)

    
    

#productFilter       




class ProductViewSet(ModelViewSet):
    permission_classes = [IsAuthenticated]
    
    filter_backends = (SearchFilter, OrderingFilter, DjangoFilterBackend)
    serializer_class=Serializer_Product
    def get_queryset(self):
        queryset = Product.objects
        all= self.request.query_params.get("all")
        if all:
            return queryset.filter(name = all)
        return queryset


#Stores 
class GetStores(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        User = Stores.objects.select_related().all()
        serialize = Serializer_Store(User, many=True)
        return Response(serialize.data)
    
class AddStores(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = Serializer_Store(data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({"status": "success","data": serializer.data}, status=status.HTTP_201_CREATED)
        else:
            return Response({"status": "error", "data": serializer.errors})


class UpdateStores(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, id=None):
        User = Stores.objects.get(id=id)
        serializer = Serializer_Store(User, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save(modified_by=request.user.username)
            return Response({"status": "success", "data": serializer.data}, status=status.HTTP_200_OK)
        else:
            return Response({"status": "error", "data": serializer.errors})


class DeleteStores(APIView): 
    permission_classes = [IsAuthenticated]
    
    def delete(self, request, id=None):
        User = get_object_or_404(Stores, id=id)
        User.delete()
        return Response({"status": "success", "data": "Deleted"})




class Adding_Multiple_Store(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset=Stores.objects.all()
    serializer_class=Serializer_Store
    def post(self, request, *args, **kwargs):
        Store_Name = dict((request.data).lists())['Store_Name']
        arr = []
        for i in Store_Name:
            modified_data = i
            file_serializer = Serializer_Store(data=modified_data)
            if file_serializer.is_valid():
                file_serializer.save()
                arr.append(file_serializer.data)
            
            else:
                return Response(arr, status=status.HTTP_400_BAD_REQUEST)

# class Get_Deal(ModelViewSet):
#     filter_backends = (SearchFilter)
#     serializer_class=Serializer_Product
#     search_fields = ['discount']
#     def get_queryset(self, request, *args, **kwargs):
#         queryset = Product.objects.all()
#         keywords = self.request.query_params.get('search')
#         if keywords:
#             queryset = queryset.filter(image_keyword__in=keywords.split(','))
#         return queryset
                    
from rest_framework import filters

class Get_Deal(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Product.objects.all()
    serializer_class = Serializer_Product
    filter_backends = [filters.SearchFilter]
    search_fields = ['discount']         
    
    
#News
class GetNews(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        User = News.objects.select_related().all()
        serialize = Serializer_News(User, many=True)
        return Response(serialize.data)
    
class AddNews(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = Serializer_News(data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({"status": "success","data": serializer.data}, status=status.HTTP_201_CREATED)
        else:
            return Response({"status": "error", "data": serializer.errors})


class UpdateNews(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, id=None):
        User = News.objects.get(id=id)
        serializer = Serializer_News(User, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save(modified_by=request.user.username)
            return Response({"status": "success", "data": serializer.data}, status=status.HTTP_200_OK)
        else:
            return Response({"status": "error", "data": serializer.errors})


class DeleteNews(APIView): 
    permission_classes = [IsAuthenticated]
    
    def delete(self, request, id=None):
        User = get_object_or_404(News, id=id)
        User.delete()
        return Response({"status": "success", "data": "Deleted"})
    
    
    
#NET Weight 
class GetNet_Weight(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        User = Net_Weight.objects.select_related().all()
        serialize = Serializer_Net_Weight(User, many=True)
        return Response(serialize.data)
    
class AddNet_Weight(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = Serializer_Net_Weight(data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({"status": "success","data": serializer.data}, status=status.HTTP_201_CREATED)
        else:
            return Response({"status": "error", "data": serializer.errors})


class UpdateNet_Weight(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, id=None):
        User = Net_Weight.objects.get(id=id)
        serializer = Serializer_Net_Weight(User, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save(modified_by=request.user.username)
            return Response({"status": "success", "data": serializer.data}, status=status.HTTP_200_OK)
        else:
            return Response({"status": "error", "data": serializer.errors})


class DeleteNet_Weight(APIView): 
    permission_classes = [IsAuthenticated]
    
    def delete(self, request, id=None):
        User = get_object_or_404(Net_Weight, id=id)
        User.delete()
        return Response({"status": "success", "data": "Deleted"})


#Flavours 
class GetFlavours(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        User = Flavours.objects.select_related().all()
        serialize = Serializer_Flavour(User, many=True)
        return Response(serialize.data)
    
class AddFlavours(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = Serializer_Flavour(data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({"status": "success","data": serializer.data}, status=status.HTTP_201_CREATED)
        else:
            return Response({"status": "error", "data": serializer.errors})


class UpdateFlavours(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, id=None):
        User = Flavours.objects.get(id=id)
        serializer = Serializer_Flavour(User, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save(modified_by=request.user.username)
            return Response({"status": "success", "data": serializer.data}, status=status.HTTP_200_OK)
        else:
            return Response({"status": "error", "data": serializer.errors})


class DeleteFlavours(APIView): 
    permission_classes = [IsAuthenticated]
    
    def delete(self, request, id=None):
        User = get_object_or_404(Flavours, id=id)
        User.delete()
        return Response({"status": "success", "data": "Deleted"})




# Api_key='rur5zqul21px64yq18i9l1h7hqdki9nwbr488hqd1qshevo3'

#################################################################################################################################################################################
################################################################TESTING##########################################################################################################
#################################################################################################################################################################################
#Coupon
from django_filters import FilterSet, NumberFilter
from django.apps import apps


class CouponFilter(FilterSet):
    min_value = NumberFilter(name='value', lookup_expr='gte')
    max_value = NumberFilter(name='value', lookup_expr='lte')

    class Meta:
        model = apps.get_model('coupons.Coupon')
        fields = ['user', 'bound', 'type', 'min_value', 'max_value']
        
from django.conf import settings
from django.contrib.auth.decorators import user_passes_test
from django.utils.decorators import method_decorator
from rest_framework.decorators import action

from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, status, viewsets

from .views import CouponFilter
from .Coupoun import Coupon,ClaimedCoupon
from .serializer import CouponSerializer,ClaimedCouponSerializer,ClaimGiftVoucher,GiftVoucher


def group_required(api_command):
    def in_groups(u):
        if u.is_authenticated():
            if u.is_superuser:
                return True

            if settings.COUPON_PERMISSIONS and api_command in settings.COUPON_PERMISSIONS:
                group_names = settings.COUPON_PERMISSIONS[api_command]

                if len(group_names) == 0:
                    return True

                if bool(u.groups.filter(name__in=group_names)):
                    return True
        return False
    return user_passes_test(in_groups)


def get_redeemed_queryset(user, coupon_id=None):
    api_command = 'REDEEMED'

    if coupon_id is None:
        qs_all = ClaimedCoupon.objects.all()
        qs_some = ClaimedCoupon.objects.filter(user=user.id)
    else:
        qs_all = ClaimedCoupon.objects.filter(coupon=coupon_id)
        qs_some = ClaimedCoupon.objects.filter(coupon=coupon_id, user=user.id)

    if user.is_superuser:
        return qs_all

    if settings.COUPON_PERMISSIONS and api_command in settings.COUPON_PERMISSIONS:
        group_names = settings.COUPON_PERMISSIONS[api_command]

        if len(group_names) == 0:
            return qs_some

        if bool(user.groups.filter(name__in=group_names)):
            return qs_all

    return qs_some


class CouponViewSet(viewsets.ModelViewSet):

    filter_backends = (filters.SearchFilter, DjangoFilterBackend)
    filter_class = CouponFilter
    search_fields = ('code', 'code_l')
    serializer_class = CouponSerializer

    def get_queryset(self):

        api_command = 'LIST'
        qs_all = Coupon.objects.all()
        qs_some = Coupon.objects.filter(bound=True, user=self.request.user.id)

        if self.request.user.is_superuser:
            return qs_all

        if settings.COUPON_PERMISSIONS and api_command in settings.COUPON_PERMISSIONS:
            group_names = settings.COUPON_PERMISSIONS[api_command]

            if len(group_names) == 0:
                return qs_some

            if bool(self.request.user.groups.filter(name__in=group_names)):
                return qs_all

        return qs_some

    @method_decorator(group_required('CREATE'))
    def create(self, request, **kwargs):
        serializer = CouponSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @method_decorator(group_required('DELETE'))
    def destroy(self, request, pk=None, **kwargs):
        coupon = get_object_or_404(Coupon.objects.all(), pk=pk)
        coupon.delete()

        return Response(status=status.HTTP_204_NO_CONTENT)

    def partial_update(self, request, pk=None, **kwargs):
        return Response(status=status.HTTP_404_NOT_FOUND)

    def retrieve(self, request, pk=None, **kwargs):
        value_is_int = False

        try:
            pk = int(pk)
            value_is_int = True
        except ValueError:
            pass

        if value_is_int:
            coupon = get_object_or_404(Coupon.objects.all(), pk=pk)
        else:
            coupon = get_object_or_404(Coupon.objects.all(), code_l=pk.lower())

        serializer = CouponSerializer(coupon, context={'request': request})

        return Response(serializer.data)

    @method_decorator(group_required('UPDATE'))
    def update(self, request, pk=None, **kwargs):
        coupon = get_object_or_404(Coupon.objects.all(), pk=pk)

        serializer = CouponSerializer(coupon, data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_202_ACCEPTED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False,methods=['get'])
    def redeemed(self, request, pk=None, **kwargs):

        coupon = get_object_or_404(Coupon.objects.all(), pk=pk)
        qs = get_redeemed_queryset(self.request.user, coupon.id)

        serializer = ClaimedCouponSerializer(qs, many=True, context={'request': request})

        return Response(serializer.data)

    @action(detail=False,methods=['put'])
    def redeem(self, request, pk=None, **kwargs):

        queryset = Coupon.objects.all()
        coupon = get_object_or_404(queryset, pk=pk)
        data = {
            'coupon': pk,
            'user':   self.request.user.id,
        }

        serializer = ClaimedCouponSerializer(data=data, context={'request': request})
        if serializer.is_valid():
            serializer.save()

            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ClaimedCouponViewSet(viewsets.ModelViewSet):
    filter_backends = (DjangoFilterBackend,)
    filter_fields = ('user',)
    serializer_class = ClaimedCouponSerializer

    def get_queryset(self):
        return get_redeemed_queryset(self.request.user)

    def create(self, request, **kwargs):
        return Response(status=status.HTTP_404_NOT_FOUND)

    @method_decorator(group_required('DELETE'))
    def destroy(self, request, pk=None, **kwargs):

        redeemed = get_object_or_404(ClaimedCoupon.objects.all(), pk=pk)
        redeemed.delete()

        return Response(status=status.HTTP_204_NO_CONTENT)

    def partial_update(self, request, pk=None, **kwargs):
        return Response(status=status.HTTP_404_NOT_FOUND)

    def retrieve(self, request, pk=None, **kwargs):
        return Response(status=status.HTTP_404_NOT_FOUND)

    def update(self, request, pk=None, **kwargs):
        return Response(status=status.HTTP_404_NOT_FOUND)



class GiftVoucherFilter(FilterSet):
    min_value = NumberFilter(name='value', lookup_expr='gte')
    max_value = NumberFilter(name='value', lookup_expr='lte')

    class Meta:
        model = GiftVoucher
        fields = '__all__'

def group_required(api_command):
    def in_groups(u):
        if u.is_authenticated():
            if u.is_superuser:
                return True

            if settings.GiftVoucher_PERMISSIONS and api_command in settings.GiftVoucher_PERMISSIONS:
                group_names = settings.GiftVoucher_PERMISSIONS[api_command]

                if len(group_names) == 0:
                    return True

                if bool(u.groups.filter(name__in=group_names)):
                    return True
        return False
    return user_passes_test(in_groups)


def get_redeemed_queryset(user, GiftVoucher_id=None):
    api_command = 'REDEEMED'

    if GiftVoucher_id is None:
        qs_all = ClaimGiftVoucher.objects.all()
        qs_some = ClaimGiftVoucher.objects.filter(user=user.id)
    else:
        qs_all = ClaimGiftVoucher.objects.filter(coupon=GiftVoucher_id)
        qs_some = ClaimGiftVoucher.objects.filter(coupon=GiftVoucher_id, user=user.id)

    if user.is_superuser:
        return qs_all

    if settings.GiftVoucher_PERMISSIONS and api_command in settings.GiftVoucher_PERMISSIONS:
        group_names = settings.GiftVoucher_PERMISSIONS[api_command]

        if len(group_names) == 0:
            return qs_some

        if bool(user.groups.filter(name__in=group_names)):
            return qs_all

    return qs_some


class GiftVoucherViewSet(viewsets.ModelViewSet):

    filter_backends = (filters.SearchFilter, DjangoFilterBackend)
    filter_class = GiftVoucherFilter
    search_fields = ('code', 'code_l')
    serializer_class = GiftVoucherSerializer

    def get_queryset(self):

        api_command = 'LIST'
        qs_all = GiftVoucher.objects.all()
        qs_some = GiftVoucher.objects.filter(bound=True, user=self.request.user.id)

        if self.request.user.is_superuser:
            return qs_all

        if settings.GiftVoucher_PERMISSIONS and api_command in settings.GiftVoucher_PERMISSIONS:
            group_names = settings.GiftVoucher_PERMISSIONS[api_command]

            if len(group_names) == 0:
                return qs_some

            if bool(self.request.user.groups.filter(name__in=group_names)):
                return qs_all

        return qs_some

    @method_decorator(group_required('CREATE'))
    def create(self, request, **kwargs):
        serializer = GiftVoucherSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @method_decorator(group_required('DELETE'))
    def destroy(self, request, pk=None, **kwargs):
        GiftVoucher = get_object_or_404(GiftVoucher.objects.all(), pk=pk)
        GiftVoucher.delete()

        return Response(status=status.HTTP_204_NO_CONTENT)

    def partial_update(self, request, pk=None, **kwargs):
        return Response(status=status.HTTP_404_NOT_FOUND)

    def retrieve(self, request, pk=None, **kwargs):
        value_is_int = False

        try:
            pk = int(pk)
            value_is_int = True
        except ValueError:
            pass

        if value_is_int:
            GiftVoucher = get_object_or_404(GiftVoucher.objects.all(), pk=pk)
        else:
            GiftVoucher = get_object_or_404(GiftVoucher.objects.all(), code_l=pk.lower())

        serializer = GiftVoucherSerializer(GiftVoucher, context={'request': request})

        return Response(serializer.data)

    @method_decorator(group_required('UPDATE'))
    def update(self, request, pk=None, **kwargs):
        GiftVoucher = get_object_or_404(GiftVoucher.objects.all(), pk=pk)

        serializer = GiftVoucherSerializer(GiftVoucher, data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_202_ACCEPTED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False,methods=['get'])
    def redeemed(self, request, pk=None, **kwargs):

        GiftVoucher = get_object_or_404(GiftVoucher.objects.all(), pk=pk)
        qs = get_redeemed_queryset(self.request.user, GiftVoucher.id)

        serializer = ClaimGiftVoucher(qs, many=True, context={'request': request})

        return Response(serializer.data)

    @action(detail=False,methods=['put'])
    def redeem(self, request, pk=None, **kwargs):

        queryset = GiftVoucher.objects.all()
        GiftVoucher = get_object_or_404(queryset, pk=pk)
        data = {
            'GiftVoucher': pk,
            'user':   self.request.user.id,
        }

        serializer = ClaimedGiftVoucherSerializer(data=data, context={'request': request})
        if serializer.is_valid():
            serializer.save()

            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ClaimGiftVoucherViewSet(viewsets.ModelViewSet):
    filter_backends = (DjangoFilterBackend,)
    filter_fields = ('user',)
    serializer_class = ClaimedGiftVoucherSerializer

    def get_queryset(self):
        return get_redeemed_queryset(self.request.user)

    def create(self, request, **kwargs):
        return Response(status=status.HTTP_404_NOT_FOUND)

    @method_decorator(group_required('DELETE'))
    def destroy(self, request, pk=None, **kwargs):

        redeemed = get_object_or_404(ClaimGiftVoucher.objects.all(), pk=pk)
        redeemed.delete()

        return Response(status=status.HTTP_204_NO_CONTENT)

    def partial_update(self, request, pk=None, **kwargs):
        return Response(status=status.HTTP_404_NOT_FOUND)

    def retrieve(self, request, pk=None, **kwargs):
        return Response(status=status.HTTP_404_NOT_FOUND)

    def update(self, request, pk=None, **kwargs):
        return Response(status=status.HTTP_404_NOT_FOUND)


import pandas as pd
import uuid

class ExportImportExcel(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self,request):
        User = Product.objects.all()
        serialize = Serializer_Product(User, many=True)
        df=pd.DataFrame(serialize.data)
        df.to_csv(f'/home/selnoxinfotech/Ecommerce/media/excel{uuid.uuid4()}.csv',encoding="UTF-8",index=False)
        return Response(serialize.data)
    
    
    
####################################################################################################################################
###################Count############################################################################################################
####################################################################################################################################

class GetCountCategories(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        count=Category.objects.all().count()
        return Response(count)
    


class GetCountSubCategories(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        count=SubCategory.objects.all().count()
        return Response(count)
    

class GetCountProduct(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        count=Product.objects.all().count()
        return Response(count)
    
class GetCountBrand(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        count=Brand.objects.all().count()
        return Response(count)
    
class GetCountStore(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        count=Stores.objects.all().count()
        return Response(count)
    
class GetCountNews(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        count=News.objects.all().count()
        return Response(count)
    

    
