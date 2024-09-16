from django.shortcuts import render
from rest_framework import viewsets, permissions, status, generics
from .serializers import *
from .models import * 
from rest_framework.response import Response 
from django.contrib.auth import get_user_model, authenticate
from knox.models import AuthToken
from rest_framework.views import APIView

from rest_framework.decorators import api_view
from rest_framework.permissions import IsAuthenticated


User = get_user_model()

class LoginViewset(viewsets.ViewSet):
    permission_classes = [permissions.AllowAny]
    serializer_class = LoginSerializer

    def create(self, request): 
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid(): 
            email = serializer.validated_data['email']
            password = serializer.validated_data['password']
            user = authenticate(request, email=email, password=password)
            if user: 
                _, token = AuthToken.objects.create(user)                
                # Return user data using UserSerializer
                user_data = UserSerializer(user).data
                
                return Response(
                    {
                        "user": user_data,  # Include user data in the response
                        "token": token
                    }
                )
            else: 
                return Response({"error": "Invalid credentials"}, status=401)    
        else: 
            return Response(serializer.errors, status=400)


class RegisterViewset(viewsets.ViewSet):
    permission_classes = [permissions.AllowAny]
    queryset = CustomUser.objects.all()
    serializer_class = RegisterSerializer

    def create(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Registration successful!"}, status=201)
        else:
            return Response(serializer.errors, status=400)


# class UserViewset(viewsets.ViewSet):
#     permission_classes = [permissions.IsAuthenticated]
#     queryset = User.objects.all()
#     serializer_class = RegisterSerializer



class UserDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        serializer = CustomUserSerializer(user)
        return Response(serializer.data)

    def list(self, request):
        queryset = User.objects.all()
        serializer = self.serializer_class(queryset, many=True)
        return Response(serializer.data)


# @api_view(['POST'])
# def register_designer(request):
#     if request.method == 'POST':
#         serializer = DesignerRegistrationSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         else:
#             print(serializer.errors)  # This will print the validation errors
#             return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    


# class DesignerRegistrationCreateView(generics.CreateAPIView):
#     queryset = DesignerRegistration.objects.all()
#     serializer_class = DesignerRegistrationSerializer

#     def post(self, request, *args, **kwargs):
#         serializer = self.get_serializer(data=request.data)
#         if serializer.is_valid():
#             self.perform_create(serializer)
#             headers = self.get_success_headers(serializer.data)
#             return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# class ApplicationTypeViewSet(viewsets.ReadOnlyModelViewSet):
#     queryset = ApplicationType.objects.all()
#     serializer_class = ApplicationTypeSerializer

# class DesignerCategoryViewSet(viewsets.ReadOnlyModelViewSet):
#     queryset = DesignerCategory.objects.all()
#     serializer_class = DesignerCategorySerializer



class DesignerRegistrationCreateView(generics.CreateAPIView):
    queryset = DesignerRegistration.objects.all()
    serializer_class = DesignerRegistrationSerializer



class MustReadListView(generics.ListAPIView):
    queryset = MustRead.objects.all()
    serializer_class = MustReadSerializer


class UpcomingEventListView(generics.ListAPIView):
    queryset = UpcomingEvent.objects.all()
    serializer_class = UpcomingEventSerializer


class BlogListView(generics.ListAPIView):
    queryset = Blog.objects.all()
    serializer_class = BlogSerializer

