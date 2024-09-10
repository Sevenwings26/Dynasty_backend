from django.shortcuts import render
from rest_framework import viewsets, permissions, status, generics

from .serializers import *
from .models import * 
from rest_framework.response import Response 
from django.contrib.auth import get_user_model, authenticate
from knox.models import AuthToken

from rest_framework.decorators import api_view


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
                return Response(
                    {
                        "user": self.serializer_class(user).data,
                        "token": token
                    }
                )
            else: 
                return Response({"error":"Invalid credentials"}, status=401)    
        else: 
            return Response(serializer.errors,status=400)


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


class UserViewset(viewsets.ViewSet):
    permission_classes = [permissions.IsAuthenticated]
    queryset = User.objects.all()
    serializer_class = RegisterSerializer

    def list(self, request):
        queryset = User.objects.all()
        serializer = self.serializer_class(queryset, many=True)
        return Response(serializer.data)


@api_view(['POST'])
def register_designer(request):
    if request.method == 'POST':
        serializer = DesignerRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            print(serializer.errors)  # This will print the validation errors
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    


class DesignerRegistrationCreateView(generics.CreateAPIView):
    queryset = DesignerRegistration.objects.all()
    serializer_class = DesignerRegistrationSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            self.perform_create(serializer)
            headers = self.get_success_headers(serializer.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ApplicationTypeViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = ApplicationType.objects.all()
    serializer_class = ApplicationTypeSerializer

class DesignerCategoryViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = DesignerCategory.objects.all()
    serializer_class = DesignerCategorySerializer



# from rest_framework import generics
# from .models import Gallery, UpcomingEvent, Blog
# from .serializers import GallerySerializer, UpcomingEventSerializer, BlogSerializer

class GalleryListView(generics.ListAPIView):
    queryset = Gallery.objects.all()
    serializer_class = GallerySerializer


class UpcomingEventListView(generics.ListAPIView):
    queryset = UpcomingEvent.objects.all()
    serializer_class = UpcomingEventSerializer


class BlogListView(generics.ListAPIView):
    queryset = Blog.objects.all()
    serializer_class = BlogSerializer


# # API Routes
# @api_view(['GET'])
# def view_all_routes(request):
#     data = [
#         'api/gallery-views/',
#         'api/blog/',
#     ]
#     return Response(data)


# # @api_view(['GET'])
# # def userInfo(request):
# #     user = request.user
# #     serializer = UserSerializer(user)
# #     return Response(serializer.data)

# # Home Page Display Shows View
# @api_view(['GET'])
# def galleryViews(request):
#     images = Gallery.objects.all()
#     serializer = GallerySerializer(images, many=True)
#     return Response(serializer.data)

# # Blog Section View
# @api_view(['GET'])
# def blog_section(request):
#     images = Blog.objects.all()
#     serializer = BlogSerializer(images, many=True)
#     return Response(serializer.data)

# # Upcoming Event View
# # @api_view(['GET'])
# # def upcoming_event(request):
# #     images = UpcomingEvent.objects.all()
# #     serializer = UpcomingEventSerializer(images, many=True)
# #     return Response(serializer.data)



# # # views.py
# from rest_framework import generics
# # from .models import ApplicationType, DesignerCategory
# from .serializers import ApplicationTypeSerializer, DesignerCategorySerializer

# class ApplicationTypeListView(generics.ListAPIView):
#     queryset = ApplicationType.objects.all()
#     serializer_class = ApplicationTypeSerializer

# class DesignerCategoryListView(generics.ListAPIView):
#     queryset = DesignerCategory.objects.all()
#     serializer_class = DesignerCategorySerializer


# from rest_framework import viewsets
# from rest_framework.response import Response
# from rest_framework.decorators import action
# from .models import DesignerRegistration, ApplicationType, DesignerCategory
# from .serializers import DesignerRegistrationSerializer, ApplicationTypeSerializer, DesignerCategorySerializer

# class DesignerRegistrationViewSet(viewsets.ModelViewSet):
#     queryset = DesignerRegistration.objects.all()
#     serializer_class = DesignerRegistrationSerializer

# class ApplicationTypeViewSet(viewsets.ReadOnlyModelViewSet):
#     queryset = ApplicationType.objects.all()
#     serializer_class = ApplicationTypeSerializer

# class DesignerCategoryViewSet(viewsets.ReadOnlyModelViewSet):
#     queryset = DesignerCategory.objects.all()
#     serializer_class = DesignerCategorySerializer


# from rest_framework import generics
# from rest_framework.response import Response
# from rest_framework import status
# from .models import DesignerRegistration
# from .serializers import DesignerRegistrationSerializer

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


# from rest_framework import viewsets
# from .models import ApplicationType, DesignerCategory
# from .serializers import ApplicationTypeSerializer, DesignerCategorySerializer

# class ApplicationTypeViewSet(viewsets.ReadOnlyModelViewSet):
#     queryset = ApplicationType.objects.all()
#     serializer_class = ApplicationTypeSerializer

# class DesignerCategoryViewSet(viewsets.ReadOnlyModelViewSet):
#     queryset = DesignerCategory.objects.all()
#     serializer_class = DesignerCategorySerializer
