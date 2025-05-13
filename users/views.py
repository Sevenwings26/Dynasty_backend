from django.shortcuts import render
from rest_framework import viewsets, permissions, status, generics
from .serializers import *
from .models import * 
from rest_framework.response import Response 
from django.contrib.auth import get_user_model, authenticate
from knox.models import AuthToken
from rest_framework.views import APIView

# from rest_framework.decorators import api_view
from rest_framework.permissions import IsAuthenticated, AllowAny

# send mail to applicant - designer's application
from django.template.loader import render_to_string
from django.core.mail import send_mail, EmailMessage

from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
import threading


User = get_user_model()
class RegisterViewset(viewsets.ViewSet):
    permission_classes = [permissions.AllowAny]
    queryset = CustomUser.objects.all()
    serializer_class = RegisterSerializer

    @swagger_auto_schema(
        operation_summary="Register a new user",
        operation_description="Creates a new user and sends a welcome email.",
        request_body=RegisterSerializer,
        responses={
            201: openapi.Response("Registration successful! A welcome email has been sent."),
            400: "Bad request - validation failed"
        }
    )
    def create(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            user = serializer.save()

            # Render the HTML email template
            context = {
                'first_name': user.username,
            }
            html_message = render_to_string('emails/welcome_email_template.html', context)

            # Send the email
            subject = "Welcome to Our Platform"
            recipient_email = user.email
            email = EmailMessage(
                subject=subject,
                body=html_message,
                from_email='arcademw1@gmail.com',
                to=[recipient_email],
            )
            email.content_subtype = "html"  # Set the email content type to HTML

            try:
                email.send()
            except Exception as e:
                return Response({"message": "User registered but failed to send email", "error": str(e)}, status=201)

            return Response({"message": "Registration successful! A welcome email has been sent.", "username": user.username, "email": user.email}, status=201)
        else:
            return Response(serializer.errors, status=400)


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

