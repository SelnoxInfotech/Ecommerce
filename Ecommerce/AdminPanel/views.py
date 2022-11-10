from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework import generics
from .models import *
from datetime import datetime
from .serializer import *
from django.shortcuts import get_object_or_404

#Signup
from django.contrib.auth.hashers import check_password,make_password
class Signup(APIView):
    def post(self,request):
        postData=request.POST
        FirstName=postData.get('FirstName')
        LastName=postData.get('LastName')
        Username=postData.get('Username')
        Email=postData.get('Email')
        password=postData.get('password')
        Date_of_Birth=postData.get('Date_of_Birth')
        Gender=postData.get('Gender')
        value={
            'FirstName':FirstName,
            'LastName':LastName,
            'Username':Username,
            'Email':Email,
            'password':password,
            'Date_of_Birth':Date_of_Birth,
            'Gender':Gender
            
        }
        error_message=None
        user=RegisterUser(FirstName=FirstName,LastName=LastName,Username=Username,Email=Email,password=password,Date_of_Birth=Date_of_Birth,Gender=Gender)
        error_message=self.validateRegisterUser(user)
        if not error_message:
            print(FirstName,LastName,Username,Email,password)
            user.password=make_password(user.password)
            user.register()
            return Response({"status": "success","value":value}, status=status.HTTP_201_CREATED)
        else:
                return Response({"status": "error", 'values':value})
    def validateRegisterUser(self,user):
        error_message=None
        if (not user.FirstName):error_message="First Name is Required"
        elif not user.LastName:error_message="last name is required"
        elif not user.Username:error_message="username is required"
        elif not user.password:error_message="password is required"
        elif len(user.password)<5:error_message="password must be 5 char long"
        elif user.isExists():error_message="Email already registered "
        return error_message
        
            
            
            
        
        

#login
# from .serializer import MyTokenObtainPairSerializer
# from rest_framework.permissions import AllowAny
# from rest_framework_simplejwt.views import TokenObtainPairView


# class MyObtainTokenPairView(TokenObtainPairView):
#     permission_classes = (AllowAny,)
#     serializer_class = MyTokenObtainPairSerializer

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
        print("adasdasssssssssssssssssssssssssssssssss",type(serialize))
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
        
#Lab Result
class GetLabResults(APIView):
    # permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        User = LabResults.objects.select_related().all()
        serialize = Serializer_LabResult(User, many=True)
        
        return Response(serialize.data)
    
class AddLabResults(APIView):
    # permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = Serializer_LabResult(data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({"status": "success","data": serializer.data}, status=status.HTTP_201_CREATED)
        else:
            return Response({"status": "error", "data": serializer.errors})


class UpdateLabResults(APIView):
    # permission_classes = [IsAuthenticated]

    def post(self, request, id=None):
        User = LabResults.objects.get(id=id)
        serializer = Serializer_LabResult(User, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save(modified_by=request.user.username)
            return Response({"status": "success", "data": serializer.data}, status=status.HTTP_200_OK)
        else:
            return Response({"status": "error", "data": serializer.errors})


class DeleteLabResults(APIView):
        def delete(self, request, id=None):
            User = get_object_or_404(LabResults, id=id)
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