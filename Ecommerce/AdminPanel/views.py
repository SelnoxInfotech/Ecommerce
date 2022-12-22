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
from .serializer import UserSerializer,  RegisterSerializer,VerifyAccountSerializer,ChangePasswordSerializer,PasswordReseetSerializer
from django.contrib.auth import login
from django.contrib.auth.models import User

from rest_framework.authtoken.serializers import AuthTokenSerializer
from knox.views import LoginView as KnoxLoginView
from .tokens import create_jwt_pair_for_user

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
    
# from django.contrib.auth import authenticate
    
class VerifyOtpLogin(APIView):
    permission_classes=(permissions.AllowAny,)
    def post(self,request):
        try:
            data=request.data

            email=request.data.get("email")
            
            otp=request.data.get("OTP")
            
            user= User.objects.filter(email=email)
            if user[0].otp != otp:
                return Response({
                    'message':'Something goes wrong',
                    'data':'invalid Otp'
                })
            user= User.objects.get(email=email)  
            if user is not None:

                tokens = create_jwt_pair_for_user(user)

                response = {"message": "Login Successfull", "tokens": tokens}
                return Response(data=response, status=status.HTTP_200_OK)

            else:
                return Response(data={"message": "Invalid email or password"})
        except Exception as e:
            return Response({'error' : str(e)},status=500)
        
        
    def get(self, request):
        try:
            content = {"user": str(request.user), "auth": str(request.auth)}

            return Response(data=content, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error' : str(e)},status=500)
    
        
class ResetPasswordAPI(APIView):
    serializer_class = ChangePasswordSerializer
    model = User

    def get_object(self, queryset=None):
        try:
            obj = self.request.user
            return obj
        except Exception as e:
            return Response({'error' : str(e)},status=500)
    

    def post(self, request, *args, **kwargs):
        try:
            self.object = self.get_object()
            serializer = ChangePasswordSerializer(data=request.data)
            if serializer.is_valid():
                email=serializer.validated_data['email']
                send_OneToOneMail(from_email='smtpselnox@gmail.com',to_emails=email)
                response = {
                    'status': 'success',
                    'code': status.HTTP_200_OK,
                    'message': 'mail sent successfully',
                    'data': {"Otp_Sent_To":email}
                }

                return Response(response)
            else:
                return Response({"message":"Something Goes Wrong"},status=400)
        except Exception as e:
            return Response({'error' : str(e)},status=500)
        
        
class VerifyOtpResetPassword(APIView):
    def get_object(self, queryset=None):
        try:
            obj = self.request.user
            return obj
        except Exception as e:
            return Response({'error' : str(e)},status=500)

    def post(self,request):
        try:
            self.object = self.get_object()
            data=request.data
            serializer=PasswordReseetSerializer(data=data)
            if serializer.is_valid():
                email=serializer.validated_data['email']
                new_password=serializer.validated_data['new_password']
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
                if len(new_password)>5 :
                    self.object.set_password(serializer.data.get("new_password"))
                    self.object.save()

                    return Response({
                            'message':'Password is Update',
                        })
                else:
                    return Response({
                                'message':'Password must be Strong',
                            })
        except Exception as e:
            return Response({'error' : str(e)},status=500)
        

class LoginAPI(KnoxLoginView):
    permission_classes=(permissions.AllowAny,)
    def post(self,request,format=None):
        try:
            serializer=AuthTokenSerializer(data=request.data)
            if serializer.is_valid():
                email=serializer.validated_data['email']
                send_OneToOneMail(from_email='smtpselnox@gmail.com',to_emails=email)
                return Response({
                            'message':'Email sent',
                            'data':{"Otp_Sent_to":email}
                        })
            else:
                return Response(serializer.errors,status=400)
        except Exception as e:
            return Response({'error' : str(e)},status=500)


# Get User API
class UserAPI(generics.RetrieveAPIView):
    permission_classes = [permissions.IsAuthenticated,]
    serializer_class = UserSerializer

    def get_object(self):
        try:
            return self.request.user
        except Exception as e:
            return Response({'error' : str(e)},status=500)
    
    
    
#Class based view to register user
class RegisterAPI(generics.GenericAPIView):
    serializer_class =RegisterSerializer

    def post(self,request,*args,**kwargs):
        try:
            serializer=self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            user=serializer.save()
            
        
            return Response({
            "user":UserSerializer(user,context=self.get_serializer_context()).data,
            "token":AuthToken.objects.create(user)[1]
            })
        except Exception as e:
            return Response({'error' : str(e)},status=500)
#Category Api
class GetCategories(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        try:
            User = Category.objects.select_related().all()
            serialize = Serializer_Category(User, many=True)
            
            return Response(serialize.data)
        except Exception as e:
            return Response({'error' : str(e)},status=500)
    
    
    
    
class AddCategories(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            serializer = Serializer_Category(data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response({"status": "success","data": serializer.data}, status=status.HTTP_201_CREATED)
            else:
                return Response({"status": "error", "data": serializer.errors},status=400)
        except Exception as e:
            return Response({'error' : str(e)},status=500)

class UpdateCategories(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, id=None):
        try:
            User = Category.objects.get(id=id)
            serializer = Serializer_Category(User, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save(modified_by=request.user.username)
                return Response({"status": "success", "data": serializer.data}, status=status.HTTP_200_OK)
            else:
                return Response({"status": "error", "data": serializer.errors},status=400)
        except Exception as e:
            return Response({'error' : str(e)},status=500)

class DeleteCategory(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request, id=None):
        try:
            User = get_object_or_404(Category, id=id)
            User.delete()
            return Response({"status": "success", "data": "Deleted"})
        except Exception as e:
            return Response({'error' : str(e)},status=500)
 
 
#Sub Category Api
class GetSubCategories(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        try:
            User = SubCategory.objects.select_related().all()
            serialize = Serializer_SubCategory(User, many=True)
            return Response(serialize.data)
        except Exception as e:
            return Response({'error' : str(e)},status=500)

class AddSubCategories(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            serializer = Serializer_SubCategory(data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response({"status": "success","data": serializer.data}, status=status.HTTP_201_CREATED)
            else:
                return Response({"status": "error", "data": serializer.errors},status=400)
        except Exception as e:
            return Response({'error' : str(e)},status=500)


class UpdateSubCategories(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, id=None):
        try:
            User = SubCategory.objects.get(id=id)
            serializer = Serializer_SubCategory(User, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save(modified_by=request.user.username)
                return Response({"status": "success", "data": serializer.data}, status=status.HTTP_200_OK)
            else:
                return Response({"status": "error", "data": serializer.errors},status=400)
        except Exception as e:
            return Response({'error' : str(e)},status=500)


class DeleteSubCategory(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request, id=None):
        try:
            User = get_object_or_404(SubCategory, id=id)
            User.delete()
            return Response({"status": "success", "data": "Deleted"})
        except Exception as e:
            return Response({'error' : str(e)},status=500)



#Country
class GetCountry(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        try:
            User = Countries.objects.select_related().all()
            serialize = Serializer_Country(User, many=True)
            
            return Response(serialize.data)
        except Exception as e:
            return Response({'error' : str(e)},status=500)
    
    
class AddCountry(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            serializer = Serializer_Country(data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response({"status": "success","data": serializer.data}, status=status.HTTP_201_CREATED)
            else:
                return Response({"status": "error", "data": serializer.errors},status=400)
        except Exception as e:
            return Response({'error' : str(e)},status=500)


class UpdateCountry(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, id=None):
        try:
            User = Countries.objects.get(id=id)
            serializer = Serializer_Country(User, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save(modified_by=request.user.username)
                return Response({"status": "success", "data": serializer.data}, status=status.HTTP_200_OK)
            else:
                return Response({"status": "error", "data": serializer.errors},status=400)
        except Exception as e:
            return Response({'error' : str(e)},status=500)


class DeleteCountry(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request, id=None):
        try:
            User = get_object_or_404(Countries, id=id)
            User.delete()
            return Response({"status": "success", "data": "Deleted"})
        except Exception as e:
            return Response({'error' : str(e)},status=500)
    
    
#States
class GetStates(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        try:
            User = States.objects.select_related().all()
            serialize = Serializer_States(User, many=True)
            
            return Response(serialize.data)
        except Exception as e:
            return Response({'error' : str(e)},status=500)
    
class AddStates(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            serializer = Serializer_States(data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response({"status": "success","data": serializer.data}, status=status.HTTP_201_CREATED)
            else:
                return Response({"status": "error", "data": serializer.errors},status=400)
        except Exception as e:
            return Response({'error' : str(e)},status=500)


class UpdateStates(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, id=None):
        try:
            User = States.objects.get(id=id)
            serializer = Serializer_States(User, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save(modified_by=request.user.username)
                return Response({"status": "success", "data": serializer.data}, status=status.HTTP_200_OK)
            else:
                return Response({"status": "error", "data": serializer.errors},status=400)
        except Exception as e:
            return Response({'error' : str(e)},status=500)


class DeleteStates(APIView):
    permission_classes = [IsAuthenticated]
    def delete(self, request, id=None):
        try:
            User = get_object_or_404(States, id=id)
            User.delete()
            return Response({"status": "success", "data": "Deleted"})
        except Exception as e:
            return Response({'error' : str(e)},status=500)
    
    
#Cities 
class GetCities(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        try:
            User = Cities.objects.select_related().all()
            serialize = Serializer_Cities(User, many=True)
            
            return Response(serialize.data)
        except Exception as e:
            return Response({'error' : str(e)},status=500)
    
class AddCities(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            serializer = Serializer_Cities(data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response({"status": "success","data": serializer.data}, status=status.HTTP_201_CREATED)
            else:
                return Response({"status": "error", "data": serializer.errors},status=400)
        except Exception as e:
            return Response({'error' : str(e)},status=500)


class UpdateCities(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, id=None):
        try:
            User = Cities.objects.get(id=id)
            serializer = Serializer_Cities(User, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save(modified_by=request.user.username)
                return Response({"status": "success", "data": serializer.data}, status=status.HTTP_200_OK)
            else:
                return Response({"status": "error", "data": serializer.errors},status=400)
        except Exception as e:
            return Response({'error' : str(e)},status=500)


class DeleteCities(APIView):
    permission_classes = [IsAuthenticated]
    def delete(self, request, id=None):
        try:
            User = get_object_or_404(Cities, id=id)
            User.delete()
            return Response({"status": "success", "data": "Deleted"})
        except Exception as e:
            return Response({'error' : str(e)},status=500)
        
#Product
class GetProduct(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        try:
            User = Product.objects.select_related().all()
            serialize = Serializer_Product(User, many=True)
            
            return Response(serialize.data)
        except Exception as e:
            return Response({'error' : str(e)},status=500)

class AddProduct(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            serializer = Serializer_Product(data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response({"status": "success","data": serializer.data}, status=status.HTTP_201_CREATED)
            else:
                return Response({"status": "error", "data": serializer.errors},status=400)
        except Exception as e:
            return Response({'error' : str(e)},status=500)
        

class UpdateProduct(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, id=None):
        try:
            User = Product.objects.get(id=id)
            serializer = Serializer_Product(User, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save(modified_by=request.user.username)
                return Response({"status": "success", "data": serializer.data}, status=status.HTTP_200_OK)
            else:
                return Response({"status": "error", "data": serializer.errors},status=400)
        except Exception as e:
            return Response({'error' : str(e)},status=500)


class DeleteProduct(APIView):
    permission_classes = [IsAuthenticated]
    def delete(self, request, id=None):
        try:
            User = get_object_or_404(Product, id=id)
            User.delete()
            return Response({"status": "success", "data": "Deleted"})
        except Exception as e:
            return Response({'error' : str(e)},status=500)
        
        
#Brand
class GetBrand(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        try:
            User = Brand.objects.select_related().all()
            serialize = Serializer_Brand(User, many=True)
            
            return Response(serialize.data)
        except Exception as e:
            return Response({'error' : str(e)},status=500)
    
class AddBrand(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            serializer = Serializer_Brand(data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response({"status": "success","data": serializer.data}, status=status.HTTP_201_CREATED)
            else:
                return Response({"status": "error", "data": serializer.errors},status=400)
        except Exception as e:
            return Response({'error' : str(e)},status=500)


class UpdateBrand(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, id=None):
        try:
            User = Brand.objects.get(id=id)
            serializer = Serializer_Brand(User, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save(modified_by=request.user.username)
                return Response({"status": "success", "data": serializer.data}, status=status.HTTP_200_OK)
            else:
                return Response({"status": "error", "data": serializer.errors},status=400)
        except Exception as e:
            return Response({'error' : str(e)},status=500)


class DeleteBrand(APIView): 
    permission_classes = [IsAuthenticated]
    def delete(self, request, id=None):
        try:
            User = get_object_or_404(Brand, id=id)
            User.delete()
            return Response({"status": "success", "data": "Deleted"})
        except Exception as e:
            return Response({'error' : str(e)},status=500)
        

#tax
class GetTax(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        try:
            User = taxes.objects.select_related().all()
            serialize = Serializer_tax(User, many=True)
            return Response(serialize.data)
        except Exception as e:
            return Response({'error' : str(e)},status=500)
    
class AddTax(APIView): 
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            serializer = Serializer_tax(data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response({"status": "success","data": serializer.data}, status=status.HTTP_201_CREATED)
            else:
                return Response({"status": "error", "data": serializer.errors},status=400)
        except Exception as e:
            return Response({'error' : str(e)},status=500)


class UpdateTax(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, id=None):
        try:
            User = taxes.objects.get(id=id)
            serializer = Serializer_tax(User, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save(modified_by=request.user.username)
                return Response({"status": "success", "data": serializer.data}, status=status.HTTP_200_OK)
            else:
                return Response({"status": "error", "data": serializer.errors},status=400)
        except Exception as e:
            return Response({'error' : str(e)},status=500)


class DeleteTax(APIView): 
    permission_classes = [IsAuthenticated]
    
    def delete(self, request, id=None):
        try:
            User = get_object_or_404(taxes, id=id)
            User.delete()
            return Response({"status": "success", "data": "Deleted"})
        except Exception as e:
            return Response({'error' : str(e)},status=500)
    



#Discount
class GetDiscount(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        try:
            User = Discount.objects.select_related().all()
            serialize = Serializer_Discount(User, many=True)
            return Response(serialize.data)
        except Exception as e:
            return Response({'error' : str(e)},status=500)
        
class AddDiscount(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            serializer = Serializer_Discount(data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response({"status": "success","data": serializer.data}, status=status.HTTP_201_CREATED)
            else:
                return Response({"status": "error", "data": serializer.errors},status=400)
        except Exception as e:
            return Response({'error' : str(e)},status=500)


class UpdateDiscount(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, id=None):
        try:
            User = Discount.objects.get(id=id)
            serializer = Serializer_Discount(User, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save(modified_by=request.user.username)
                return Response({"status": "success", "data": serializer.data}, status=status.HTTP_200_OK)
            else:
                return Response({"status": "error", "data": serializer.errors},status=400)
        except Exception as e:
            return Response({'error' : str(e)},status=500)


class DeleteDiscount(APIView): 
    permission_classes = [IsAuthenticated]
    
    def delete(self, request, id=None):
        try:
            User = get_object_or_404(Discount, id=id)
            User.delete()
            return Response({"status": "success", "data": "Deleted"})
        except Exception as e:
            return Response({'error' : str(e)},status=500)


     
#Replicate or Duplicate Data
class Replicate_data(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request, id=None):
        try:
            User = Product.objects.get(id=id)
            serializer = Serializer_Product(User, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response({"status": "success", "data": serializer.data}, status=status.HTTP_200_OK)
            else:
                return Response({"status": "error", "data": serializer.errors},status=400)
        except Exception as e:
            return Response({'error' : str(e)},status=500)    
        
        
# Adding Multiple Images
def modify_input_for_multiple_files(image):
    dict = {}
    dict['Multiple_Image'] = image
    return dict

class MultipleImageUpload(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset=Product.objects.all()
    serializer_class=Serializer_Product
    def post(self, request, *args, **kwargs):
        try:
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
                return Response(arr, status=400)
        except Exception as e:
            return Response({'error' : str(e)},status=500)

    
    

#productFilter       




class ProductViewSet(ModelViewSet):
    permission_classes = [IsAuthenticated]
    
    filter_backends = (SearchFilter, OrderingFilter, DjangoFilterBackend)
    serializer_class=Serializer_Product
    def get_queryset(self):
        try:
            queryset = Product.objects
            all= self.request.query_params.get("all")
            if all:
                return queryset.filter(name = all)
            return queryset
        except Exception as e:
            return Response({'error' : str(e)},status=500)


#Stores 
class GetStores(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        try:
            User = Stores.objects.select_related().all()
            serialize = Serializer_Store(User, many=True)
            return Response(serialize.data)
        except Exception as e:
            return Response({'error' : str(e)},status=500)
    
class AddStores(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            serializer = Serializer_Store(data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response({"status": "success","data": serializer.data}, status=status.HTTP_201_CREATED)
            else:
                return Response({"status": "error", "data": serializer.errors},status=400)
        except Exception as e:
            return Response({'error' : str(e)},status=500)


class UpdateStores(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, id=None):
        try:
            User = Stores.objects.get(id=id)
            serializer = Serializer_Store(User, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save(modified_by=request.user.username)
                return Response({"status": "success", "data": serializer.data}, status=status.HTTP_200_OK)
            else:
                return Response({"status": "error", "data": serializer.errors},status=400)
        except Exception as e:
            return Response({'error' : str(e)},status=500)


class DeleteStores(APIView): 
    permission_classes = [IsAuthenticated]
    
    def delete(self, request, id=None):
        try:
            User = get_object_or_404(Stores, id=id)
            User.delete()
            return Response({"status": "success", "data": "Deleted"})
        except Exception as e:
            return Response({'error' : str(e)},status=500)




class Adding_Multiple_Store(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset=Stores.objects.all()
    serializer_class=Serializer_Store
    def post(self, request, *args, **kwargs):
        try:
            Store_Name = dict((request.data).lists())['Store_Name']
            arr = []
            for i in Store_Name:
                modified_data = i
                file_serializer = Serializer_Store(data=modified_data)
                if file_serializer.is_valid():
                    file_serializer.save()
                    arr.append(file_serializer.data)
                
                else:
                    return Response(arr, status=400)
        except Exception as e:
            return Response({'error' : str(e)},status=500)

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
        try:
            User = News.objects.select_related().all()
            serialize = Serializer_News(User, many=True)
            return Response(serialize.data)
        except Exception as e:
            return Response({'error' : str(e)},status=500)
    
class AddNews(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            serializer = Serializer_News(data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response({"status": "success","data": serializer.data}, status=status.HTTP_201_CREATED)
            else:
                return Response({"status": "error", "data": serializer.errors},status=400)
        except Exception as e:
            return Response({'error' : str(e)},status=500)


class UpdateNews(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, id=None):
        try:
            User = News.objects.get(id=id)
            serializer = Serializer_News(User, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save(modified_by=request.user.username)
                return Response({"status": "success", "data": serializer.data}, status=status.HTTP_200_OK)
            else:
                return Response({"status": "error", "data": serializer.errors},status=400)
        except Exception as e:
            return Response({'error' : str(e)},status=500)


class DeleteNews(APIView): 
    permission_classes = [IsAuthenticated]
    
    def delete(self, request, id=None):
        try:
            User = get_object_or_404(News, id=id)
            User.delete()
            return Response({"status": "success", "data": "Deleted"})
        except Exception as e:
            return Response({'error' : str(e)},status=500)    
    
    
#NET Weight 
class GetNet_Weight(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        try:
            User = Net_Weight.objects.select_related().all()
            serialize = Serializer_Net_Weight(User, many=True)
            return Response(serialize.data)
        except Exception as e:
            return Response({'error' : str(e)},status=500)
    
class AddNet_Weight(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            serializer = Serializer_Net_Weight(data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response({"status": "success","data": serializer.data}, status=status.HTTP_201_CREATED)
            else:
                return Response({"status": "error", "data": serializer.errors},status=400)
        except Exception as e:
            return Response({'error' : str(e)},status=500)


class UpdateNet_Weight(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, id=None):
        try:
            User = Net_Weight.objects.get(id=id)
            serializer = Serializer_Net_Weight(User, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save(modified_by=request.user.username)
                return Response({"status": "success", "data": serializer.data}, status=status.HTTP_200_OK)
            else:
                return Response({"status": "error", "data": serializer.errors},status=400)
        except Exception as e:
            return Response({'error' : str(e)},status=500)

class DeleteNet_Weight(APIView): 
    permission_classes = [IsAuthenticated]
    
    def delete(self, request, id=None):
        try:
            User = get_object_or_404(Net_Weight, id=id)
            User.delete()
            return Response({"status": "success", "data": "Deleted"})
        except Exception as e:
            return Response({'error' : str(e)},status=500)


#Flavours 
class GetFlavours(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        try:
            User = Flavours.objects.select_related().all()
            serialize = Serializer_Flavour(User, many=True)
            return Response(serialize.data)
        except Exception as e:
            return Response({'error' : str(e)},status=500)
    
class AddFlavours(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            serializer = Serializer_Flavour(data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response({"status": "success","data": serializer.data}, status=status.HTTP_201_CREATED)
            else:
                return Response({"status": "error", "data": serializer.errors},status=400)
        except Exception as e:
            return Response({'error' : str(e)},status=500)


class UpdateFlavours(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, id=None):
        try:
            User = Flavours.objects.get(id=id)
            serializer = Serializer_Flavour(User, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save(modified_by=request.user.username)
                return Response({"status": "success", "data": serializer.data}, status=status.HTTP_200_OK)
            else:
                return Response({"status": "error", "data": serializer.errors},status=400)
        except Exception as e:
            return Response({'error' : str(e)},status=500)


class DeleteFlavours(APIView): 
    permission_classes = [IsAuthenticated]
    
    def delete(self, request, id=None):
        try:
            User = get_object_or_404(Flavours, id=id)
            User.delete()
            return Response({"status": "success", "data": "Deleted"})
        except Exception as e:
            return Response({'error' : str(e)},status=500)




# Api_key='rur5zqul21px64yq18i9l1h7hqdki9nwbr488hqd1qshevo3'

#################################################################################################################################################################################
################################################################TESTING##########################################################################################################
#################################################################################################################################################################################
#Coupon
from django_filters import FilterSet, NumberFilter
from django.apps import apps
from .Coupoun import Coupon,ClaimedCoupon


class CouponFilter(FilterSet):
    min_value = NumberFilter(name='value', lookup_expr='gte')
    max_value = NumberFilter(name='value', lookup_expr='lte')

    class Meta:
        model = Coupon
        fields = ['bound', 'type', 'min_value', 'max_value']
        
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
    try:
        def in_groups(u):
            try:
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
            except Exception as e:
                return Response({'error' : str(e)},status=500)
        return user_passes_test(in_groups)
    except Exception as e:
            return Response({'error' : str(e)},status=500)


def get_redeemed_queryset(user, coupon_id=None):
    try:
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
    except Exception as e:
            return Response({'error' : str(e)},status=500)


class CouponViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]

    filter_backends = (filters.SearchFilter, DjangoFilterBackend)
    filter_class = CouponFilter
    search_fields = ('code', 'code_l')
    serializer_class = CouponSerializer

    def get_queryset(self):
        try:

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
        except Exception as e:
            return Response({'error' : str(e)},status=500)

    @method_decorator(group_required('CREATE'))
    def create(self, request, **kwargs):
        try:
            serializer = CouponSerializer(data=request.data, context={'request': request})
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)

            return Response(serializer.errors, status=400)
        except Exception as e:
            return Response({'error' : str(e)},status=500)

    @method_decorator(group_required('DELETE'))
    def destroy(self, request, pk=None, **kwargs):
        try:
            coupon = get_object_or_404(Coupon.objects.all(), pk=pk)
            coupon.delete()

            return Response(status=status.HTTP_204_NO_CONTENT)
        except Exception as e:
            return Response({'error' : str(e)},status=500)

    def partial_update(self, request, pk=None, **kwargs):
        try:
            return Response(status=400)
        except Exception as e:
            return Response({'error' : str(e)},status=500)

    def retrieve(self, request, pk=None, **kwargs):
        try:
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
        except Exception as e:
            return Response({'error' : str(e)},status=500)

    @method_decorator(group_required('UPDATE'))
    def update(self, request, pk=None, **kwargs):
        try:
            coupon = get_object_or_404(Coupon.objects.all(), pk=pk)

            serializer = CouponSerializer(coupon, data=request.data, context={'request': request})
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_202_ACCEPTED)

            return Response(serializer.errors, status=200)
        except Exception as e:
            return Response({'error' : str(e)},status=500)

    @action(detail=False,methods=['get'])
    def redeemed(self, request, pk=None, **kwargs):
        try:

            coupon = get_object_or_404(Coupon.objects.all(), pk=pk)
            qs = get_redeemed_queryset(self.request.user, coupon.id)

            serializer = ClaimedCouponSerializer(qs, many=True, context={'request': request})

            return Response(serializer.data)
        except Exception as e:
            return Response({'error' : str(e)},status=500)

    @action(detail=False,methods=['put'])
    def redeem(self, request, pk=None, **kwargs):
        try:

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

            return Response(serializer.errors, status=400)
        except Exception as e:
            return Response({'error' : str(e)},status=500)


class ClaimedCouponViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    filter_backends = (DjangoFilterBackend,)
    filter_fields = ('user',)
    serializer_class = ClaimedCouponSerializer

    def get_queryset(self):
        try:
            return get_redeemed_queryset(self.request.user)
        except Exception as e:
            return Response({'error' : str(e)},status=500)

    def create(self, request, **kwargs):
        try:
            return Response(status=400)
        except Exception as e:
            return Response({'error' : str(e)},status=500)

    @method_decorator(group_required('DELETE'))
    def destroy(self, request, pk=None, **kwargs):
        try:

            redeemed = get_object_or_404(ClaimedCoupon.objects.all(), pk=pk)
            redeemed.delete()

            return Response(status=status.HTTP_204_NO_CONTENT)
        except Exception as e:
            return Response({'error' : str(e)},status=500)

    def partial_update(self, request, pk=None, **kwargs):
        try:
            return Response(status=400)
        except Exception as e:
            return Response({'error' : str(e)},status=500)

    def retrieve(self, request, pk=None, **kwargs):
        try:
            return Response(status=400)
        except Exception as e:
            return Response({'error' : str(e)},status=500)

    def update(self, request, pk=None, **kwargs):
        try:
            return Response(status=400)
        except Exception as e:
            return Response({'error' : str(e)},status=500)



class GiftVoucherFilter(FilterSet):
    min_value = NumberFilter(name='value', lookup_expr='gte')
    max_value = NumberFilter(name='value', lookup_expr='lte')

    class Meta:
        model = GiftVoucher
        fields = '__all__'

def group_required(api_command):
    try:
        def in_groups(u):
            try:
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
            except Exception as e:
                return Response({'error' : str(e)},status=500)
        return user_passes_test(in_groups)
    except Exception as e:
            return Response({'error' : str(e)},status=500)


def get_redeemed_queryset(user, GiftVoucher_id=None):
    try:
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
    except Exception as e:
            return Response({'error' : str(e)},status=500)


class GiftVoucherViewSet(viewsets.ModelViewSet):
    
    permission_classes = [IsAuthenticated]

    filter_backends = (filters.SearchFilter, DjangoFilterBackend)
    filter_class = GiftVoucherFilter
    search_fields = ('code', 'code_l')
    serializer_class = GiftVoucherSerializer

    def get_queryset(self):
        try:

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
        except Exception as e:
            return Response({'error' : str(e)},status=500)

    @method_decorator(group_required('CREATE'))
    def create(self, request, **kwargs):
        try:
            serializer = GiftVoucherSerializer(data=request.data, context={'request': request})
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)

            return Response(serializer.errors, status=400)
        except Exception as e:
            return Response({'error' : str(e)},status=500)

    @method_decorator(group_required('DELETE'))
    def destroy(self, request, pk=None, **kwargs):
        try:
            GiftVoucher = get_object_or_404(GiftVoucher.objects.all(), pk=pk)
            GiftVoucher.delete()

            return Response(status=status.HTTP_204_NO_CONTENT)
        except Exception as e:
            return Response({'error' : str(e)},status=500)

    def partial_update(self, request, pk=None, **kwargs):
        try:
            return Response(status=400)
        except Exception as e:
            return Response({'error' : str(e)},status=500)

    def retrieve(self, request, pk=None, **kwargs):
        try:
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
        except Exception as e:
            return Response({'error' : str(e)},status=500)

    @method_decorator(group_required('UPDATE'))
    def update(self, request, pk=None, **kwargs):
        try:
            GiftVoucher = get_object_or_404(GiftVoucher.objects.all(), pk=pk)

            serializer = GiftVoucherSerializer(GiftVoucher, data=request.data, context={'request': request})
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_202_ACCEPTED)

            return Response(serializer.errors, status=400)
        except Exception as e:
            return Response({'error' : str(e)},status=500)

    @action(detail=False,methods=['get'])
    def redeemed(self, request, pk=None, **kwargs):
        try:

            GiftVoucher = get_object_or_404(GiftVoucher.objects.all(), pk=pk)
            qs = get_redeemed_queryset(self.request.user, GiftVoucher.id)

            serializer = ClaimGiftVoucher(qs, many=True, context={'request': request})

            return Response(serializer.data)
        except Exception as e:
            return Response({'error' : str(e)},status=500)

    @action(detail=False,methods=['put'])
    def redeem(self, request, pk=None, **kwargs):
        try:

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

            return Response(serializer.errors, status=400)
        except Exception as e:
            return Response({'error' : str(e)},status=500)


class ClaimGiftVoucherViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    filter_backends = (DjangoFilterBackend,)
    filter_fields = ('user',)
    serializer_class = ClaimedGiftVoucherSerializer

    def get_queryset(self):
        try:
            return get_redeemed_queryset(self.request.user)
        except Exception as e:
            return Response({'error' : str(e)},status=500)

    def create(self, request, **kwargs):
        try:
            return Response(status=400)
        except Exception as e:
            return Response({'error' : str(e)},status=500)

    @method_decorator(group_required('DELETE'))
    def destroy(self, request, pk=None, **kwargs):
        try:

            redeemed = get_object_or_404(ClaimGiftVoucher.objects.all(), pk=pk)
            redeemed.delete()

            return Response(status=status.HTTP_204_NO_CONTENT)
        except Exception as e:
            return Response({'error' : str(e)},status=500)

    def partial_update(self, request, pk=None, **kwargs):
        try:
            return Response(status=400)
        except Exception as e:
            return Response({'error' : str(e)},status=500)

    def retrieve(self, request, pk=None, **kwargs):
        try:
            return Response(status=400)
        except Exception as e:
            return Response({'error' : str(e)},status=500)

    def update(self, request, pk=None, **kwargs):
        try:
            return Response(status=400)
        except Exception as e:
            return Response({'error' : str(e)},status=500)


import pandas as pd
import uuid

class ExportImportExcel(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self,request):
        try:
            User = Product.objects.all()
            serialize = Serializer_Product(User, many=True)
            df=pd.DataFrame(serialize.data)
            df.to_csv(f'/home/selnoxinfotech/Ecommerce/media/excel{uuid.uuid4()}.csv',encoding="UTF-8",index=False)
            return Response(serialize.data)
        except Exception as e:
            return Response({'error' : str(e)},status=500)
        
    
    
####################################################################################################################################
###################Count############################################################################################################
####################################################################################################################################

class GetCountCategories(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        try:
            count=Category.objects.all().count()
            return Response(count)
        except Exception as e:
            return Response({'error' : str(e)},status=500)
        


class GetCountSubCategories(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        try:
            count=SubCategory.objects.all().count()
            return Response(count)
        except Exception as e:
            return Response({'error' : str(e)},status=500)
        

class GetCountProduct(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        try:
            count=Product.objects.all().count()
            return Response(count)
        except Exception as e:
            return Response({'error' : str(e)},status=500)
        
class GetCountBrand(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        try:
            count=Brand.objects.all().count()
            return Response(count)
        except Exception as e:
            return Response({'error' : str(e)},status=500)
        
class GetCountStore(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        try:
            count=Stores.objects.all().count()
            return Response(count)
        except Exception as e:
            return Response({'error' : str(e)},status=500)
    
class GetCountNews(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        try:
            count=News.objects.all().count()
            return Response(count)
        except Exception as e:
            return Response({'error' : str(e)},status=500)
    

class TotalCount(APIView):
    permission_classes = [IsAuthenticated]
    def get(self,request,format=None):
        try:
            category=Category.objects.all().count()
            subCategory=SubCategory.objects.all().count()
            product=Product.objects.all().count()
            brand=Brand.objects.all().count()
            store=Stores.objects.all().count()
            news=News.objects.all().count()
            return Response({'Data':[{"title":"Total Category","total":category},
                                    {"title":"Total Product","total":product},
                                    {"title":"Total subCategory","total":subCategory},
                                    {"title":"Total brand","total":brand},
                                    {"title":"Total store","total":store},
                                    {"title":"Total News","total":news}]})
        except Exception as e:
            return Response({'error' : str(e)},status=500)    

from django.db.models import Count
class TotalProductGraph(APIView):   
    permission_classes = [IsAuthenticated]
    def get(self,request):
        try:
            TotalProduct=Product.objects.filter(created__range=["2022-01-01", "2050-01-31"])
            if TotalProduct is not None:
                User = Product.objects.all()
                for i in User:
                    CreatedMonths=i.created.strftime('%B')
                    if CreatedMonths=='January':
                        TotalProductCount=Product.objects.count()
                    elif CreatedMonths=='February':
                        TotalProductCount=Product.objects.count()
                    elif CreatedMonths=='March':
                        TotalProductCount=Product.objects.count()
                    elif CreatedMonths=='April':
                        TotalProductCount=Product.objects.count()
                    elif CreatedMonths=='May':
                        TotalProductCount=Product.objects.count()
                    elif CreatedMonths=='June':
                        TotalProductCount=Product.objects.count()
                    elif CreatedMonths=='July':
                        TotalProductCount=Product.objects.count()
                    elif CreatedMonths=='August':
                        TotalProductCount=Product.objects.count()
                    elif CreatedMonths=='September':
                        TotalProductCount=Product.objects.count()
                    elif CreatedMonths=='October':
                        TotalProductCount=Product.objects.count()
                    elif CreatedMonths=='November':
                        TotalProductCount=Product.objects.count()
                    elif CreatedMonths=='December':
                        TotalProductCount=Product.objects.count()
                        
            return Response({'data':{"Month":CreatedMonths,"count":TotalProductCount}})
        except Exception as e:
            return Response({'error' : str(e)},status=500)



