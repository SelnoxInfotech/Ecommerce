from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework import generics
from .models import Category,SubCategory,Countries,States,Cities,StrainType,Brand,Product,taxes,Discount
from .serializer import Serializer_Category,Serializer_SubCategory,Serializer_Country,Serializer_States,Serializer_Cities,Serializer_StrainType,Serializer_Product,Serializer_Brand,Serializer_tax,Serializer_Discount
from django.shortcuts import get_object_or_404
from rest_framework.viewsets import ModelViewSet  
from rest_framework import viewsets
from rest_framework.parsers import MultiPartParser,FormParser
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter, SearchFilter

from rest_framework.permissions import AllowAny
from .serializer import UserSerializer,RegisterSerializer
from django.contrib.auth.models import User
from rest_framework.authentication import TokenAuthentication

# Class based view to Get User Details using Token Authentication
class UserDetailAPI(APIView):
  authentication_classes = (TokenAuthentication,)
  permission_classes = (AllowAny,)
  def get(self,request,*args,**kwargs):
    user = User.objects.get(id=request.user.id)
    serializer = UserSerializer(user)
    return Response(serializer.data)

#Class based view to register user
class RegisterUserAPIView(generics.CreateAPIView):
  permission_classes = (AllowAny,)
  serializer_class = RegisterSerializer

#Category Api
class GetCategories(APIView):
    # permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        User = Category.objects.select_related().all()
        serialize = Serializer_Category(User, many=True)
        
        return Response(serialize.data)
    
class AddCategories(APIView):
    # permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = Serializer_Category(data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({"status": "success","data": serializer.data}, status=status.HTTP_201_CREATED)
        else:
            return Response({"status": "error", "data": serializer.errors})


class UpdateCategories(APIView):
    # permission_classes = [IsAuthenticated]

    def post(self, request, id=None):
        User = Category.objects.get(id=id)
        serializer = Serializer_Category(User, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save(modified_by=request.user.username)
            return Response({"status": "success", "data": serializer.data}, status=status.HTTP_200_OK)
        else:
            return Response({"status": "error", "data": serializer.errors})


class DeleteCategory(APIView):
    # permission_classes = [IsAuthenticated]

    def delete(self, request, id=None):
        User = get_object_or_404(Category, id=id)
        User.delete()
        return Response({"status": "success", "data": "Deleted"})
 
 
#Sub Category Api
class GetSubCategories(APIView):
    # permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        User = SubCategory.objects.select_related().all()
        serialize = Serializer_SubCategory(User, many=True)
        return Response(serialize.data)
    
class AddSubCategories(APIView):
    # permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = Serializer_SubCategory(data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({"status": "success","data": serializer.data}, status=status.HTTP_201_CREATED)
        else:
            return Response({"status": "error", "data": serializer.errors})


class UpdateSubCategories(APIView):
    # permission_classes = [IsAuthenticated]

    def post(self, request, id=None):
        User = SubCategory.objects.get(id=id)
        serializer = Serializer_SubCategory(User, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save(modified_by=request.user.username)
            return Response({"status": "success", "data": serializer.data}, status=status.HTTP_200_OK)
        else:
            return Response({"status": "error", "data": serializer.errors})


class DeleteSubCategory(APIView):
    # permission_classes = [IsAuthenticated]

    def delete(self, request, id=None):
        User = get_object_or_404(SubCategory, id=id)
        User.delete()
        return Response({"status": "success", "data": "Deleted"})



#Country
class GetCountry(APIView):
    # permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        User = Countries.objects.select_related().all()
        serialize = Serializer_Country(User, many=True)
        
        return Response(serialize.data)
    
class AddCountry(APIView):
    # permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = Serializer_Country(data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({"status": "success","data": serializer.data}, status=status.HTTP_201_CREATED)
        else:
            return Response({"status": "error", "data": serializer.errors})


class UpdateCountry(APIView):
    # permission_classes = [IsAuthenticated]

    def post(self, request, id=None):
        User = Countries.objects.get(id=id)
        serializer = Serializer_Country(User, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save(modified_by=request.user.username)
            return Response({"status": "success", "data": serializer.data}, status=status.HTTP_200_OK)
        else:
            return Response({"status": "error", "data": serializer.errors})


class DeleteCountry(APIView):
    # permission_classes = [IsAuthenticated]

    def delete(self, request, id=None):
        User = get_object_or_404(Countries, id=id)
        User.delete()
        return Response({"status": "success", "data": "Deleted"})
    
    
#States
class GetStates(APIView):
    # permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        User = States.objects.select_related().all()
        serialize = Serializer_States(User, many=True)
        
        return Response(serialize.data)
    
class AddStates(APIView):
    # permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = Serializer_States(data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({"status": "success","data": serializer.data}, status=status.HTTP_201_CREATED)
        else:
            return Response({"status": "error", "data": serializer.errors})


class UpdateStates(APIView):
    # permission_classes = [IsAuthenticated]

    def post(self, request, id=None):
        User = States.objects.get(id=id)
        serializer = Serializer_States(User, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save(modified_by=request.user.username)
            return Response({"status": "success", "data": serializer.data}, status=status.HTTP_200_OK)
        else:
            return Response({"status": "error", "data": serializer.errors})


class DeleteStates(APIView):
        def delete(self, request, id=None):
            User = get_object_or_404(States, id=id)
            User.delete()
            return Response({"status": "success", "data": "Deleted"})
    
    
#Cities
class GetCities(APIView):
    # permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        User = Cities.objects.select_related().all()
        serialize = Serializer_Cities(User, many=True)
        
        return Response(serialize.data)
    
class AddCities(APIView):
    # permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = Serializer_Cities(data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({"status": "success","data": serializer.data}, status=status.HTTP_201_CREATED)
        else:
            return Response({"status": "error", "data": serializer.errors})


class UpdateCities(APIView):
    # permission_classes = [IsAuthenticated]

    def post(self, request, id=None):
        User = Cities.objects.get(id=id)
        serializer = Serializer_Cities(User, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save(modified_by=request.user.username)
            return Response({"status": "success", "data": serializer.data}, status=status.HTTP_200_OK)
        else:
            return Response({"status": "error", "data": serializer.errors})


class DeleteCities(APIView):
        def delete(self, request, id=None):
            User = get_object_or_404(Cities, id=id)
            User.delete()
            return Response({"status": "success", "data": "Deleted"})
        
        
#Strain types
class GetStrainType(APIView):
    # permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        User = StrainType.objects.select_related().all()
        serialize = Serializer_StrainType(User, many=True)
        
        return Response(serialize.data)
    
class AddStrainType(APIView):
    # permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = Serializer_StrainType(data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({"status": "success","data": serializer.data}, status=status.HTTP_201_CREATED)
        else:
            return Response({"status": "error", "data": serializer.errors})


class UpdateStrainType(APIView):
    # permission_classes = [IsAuthenticated]

    def post(self, request, id=None):
        User = StrainType.objects.get(id=id)
        serializer = Serializer_StrainType(User, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save(modified_by=request.user.username)
            return Response({"status": "success", "data": serializer.data}, status=status.HTTP_200_OK)
        else:
            return Response({"status": "error", "data": serializer.errors})


class DeleteStrainType(APIView):
        def delete(self, request, id=None):
            User = get_object_or_404(StrainType, id=id)
            User.delete()
            return Response({"status": "success", "data": "Deleted"})
        
        
#Product
class GetProduct(APIView):
    # permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        User = Product.objects.select_related().all()
        serialize = Serializer_Product(User, many=True)
        
        return Response(serialize.data)
    
class AddProduct(APIView):
    # permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = Serializer_Product(data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({"status": "success","data": serializer.data}, status=status.HTTP_201_CREATED)
        else:
            return Response({"status": "error", "data": serializer.errors})
    

class UpdateProduct(APIView):
    # permission_classes = [IsAuthenticated]

    def post(self, request, id=None):
        User = Product.objects.get(id=id)
        serializer = Serializer_Product(User, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save(modified_by=request.user.username)
            return Response({"status": "success", "data": serializer.data}, status=status.HTTP_200_OK)
        else:
            return Response({"status": "error", "data": serializer.errors})


class DeleteProduct(APIView):
        def delete(self, request, id=None):
            User = get_object_or_404(Product, id=id)
            User.delete()
            return Response({"status": "success", "data": "Deleted"})
        
        
#Brand
class GetBrand(APIView):
    # permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        User = Brand.objects.select_related().all()
        serialize = Serializer_Brand(User, many=True)
        
        return Response(serialize.data)
    
class AddBrand(APIView):
    # permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = Serializer_Brand(data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({"status": "success","data": serializer.data}, status=status.HTTP_201_CREATED)
        else:
            return Response({"status": "error", "data": serializer.errors})


class UpdateBrand(APIView):
    # permission_classes = [IsAuthenticated]

    def post(self, request, id=None):
        User = Brand.objects.get(id=id)
        serializer = Serializer_Brand(User, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save(modified_by=request.user.username)
            return Response({"status": "success", "data": serializer.data}, status=status.HTTP_200_OK)
        else:
            return Response({"status": "error", "data": serializer.errors})


class DeleteBrand(APIView): 
        def delete(self, request, id=None):
            User = get_object_or_404(Brand, id=id)
            User.delete()
            return Response({"status": "success", "data": "Deleted"})
        

#tax
class GetTax(APIView):
    # permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        User = taxes.objects.select_related().all()
        serialize = Serializer_tax(User, many=True)
        return Response(serialize.data)
    
class AddTax(APIView):
    # permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = Serializer_tax(data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({"status": "success","data": serializer.data}, status=status.HTTP_201_CREATED)
        else:
            return Response({"status": "error", "data": serializer.errors})


class UpdateTax(APIView):
    # permission_classes = [IsAuthenticated]

    def post(self, request, id=None):
        User = taxes.objects.get(id=id)
        serializer = Serializer_tax(User, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save(modified_by=request.user.username)
            return Response({"status": "success", "data": serializer.data}, status=status.HTTP_200_OK)
        else:
            return Response({"status": "error", "data": serializer.errors})


class DeleteTax(APIView): 
        def delete(self, request, id=None):
            User = get_object_or_404(taxes, id=id)
            User.delete()
            return Response({"status": "success", "data": "Deleted"})
        



#Discount
class GetDiscount(APIView):
    # permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        User = Discount.objects.select_related().all()
        serialize = Serializer_Discount(User, many=True)
        return Response(serialize.data)
    
class AddDiscount(APIView):
    # permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = Serializer_Discount(data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({"status": "success","data": serializer.data}, status=status.HTTP_201_CREATED)
        else:
            return Response({"status": "error", "data": serializer.errors})


class UpdateDiscount(APIView):
    # permission_classes = [IsAuthenticated]

    def post(self, request, id=None):
        User = Discount.objects.get(id=id)
        serializer = Serializer_Discount(User, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save(modified_by=request.user.username)
            return Response({"status": "success", "data": serializer.data}, status=status.HTTP_200_OK)
        else:
            return Response({"status": "error", "data": serializer.errors})


class DeleteDiscount(APIView): 
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
    filter_backends = (SearchFilter, OrderingFilter, DjangoFilterBackend)
    serializer_class=Serializer_Product
    def get_queryset(self):
        queryset = Product.objects
        all= self.request.query_params.get("all")
        if all:
            return queryset.filter(name = all)
        return queryset




