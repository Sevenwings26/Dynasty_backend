from django.shortcuts import render
from rest_framework import viewsets, permissions, status, generics
from .serializers import *
from .models import * 
from rest_framework.response import Response 
from django.contrib.auth import get_user_model, authenticate
from knox.models import AuthToken
from rest_framework.views import APIView

# from rest_framework.decorators import api_view
from rest_framework.permissions import IsAuthenticated

# send mail to applicant - designer's application
from django.core.mail import send_mail
from django.template.loader import render_to_string

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
                user_data = CustomUserSerializer(user).data
                
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


# Exhibition application view
class ExhibitionApplicationCreateView(generics.CreateAPIView):
    queryset = ExhibitionApplication.objects.all()
    serializer_class = ExhibitionApplicationSerializer

    """ Function to send mail after a successful registration """
    def perform_create(self, serializer):
        application = serializer.save()

        # Email to the user (applicant)
        user_subject = 'Application Received'
        user_message = render_to_string('emails/user_application_received.html', {'application': application})
        user_email = application.email
        send_mail(
            subject=user_subject,
            message='Your application details have been received',  # Optional plain text fallback
            from_email='lastborn.ai@gmail.com',
            recipient_list=[user_email],
            fail_silently=False,
            html_message=user_message  # Send the HTML version of the email
        )

        # Email to the admin
        admin_subject = 'New Exhibition Application Submitted'
        admin_message = render_to_string('emails/admin_application_notification.html', {'application': application})
        send_mail(
            subject=admin_subject,
            message='A new exhibition application has been submitted',  # Optional plain text fallback
            from_email='lastborn.ai@gmail.com',
            recipient_list=['arcademw1@gmail.com'],
            fail_silently=False,
            html_message=admin_message  # Send the HTML version of the email
        )

    # Overriding the create method for a custom response
    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        return Response({'message': 'Application submitted successfully!'}, status=status.HTTP_201_CREATED)


# Must read field 
class MustReadListView(generics.ListAPIView):
    queryset = MustRead.objects.all()
    serializer_class = MustReadSerializer


class UpcomingEventListView(generics.ListAPIView):
    queryset = UpcomingEvent.objects.all()
    serializer_class = UpcomingEventSerializer


class BlogListView(generics.ListAPIView):
    queryset = Blog.objects.all()
    serializer_class = BlogSerializer

