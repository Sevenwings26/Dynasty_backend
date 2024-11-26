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
from django.core.mail import send_mail
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.utils.timezone import now

import logging
from django.utils.timezone import now
from django.core.mail import send_mail, EmailMessage
from rest_framework import generics
from django.template.loader import render_to_string
from .models import ExhibitionApplication
from .serializers import ExhibitionApplicationSerializer


User = get_user_model()


class RegisterViewset(viewsets.ViewSet):
    permission_classes = [permissions.AllowAny]
    queryset = CustomUser.objects.all()
    serializer_class = RegisterSerializer

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

            return Response({"message": "Registration successful! A welcome email has been sent."}, status=201)
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


logger = logging.getLogger(__name__)

class ExhibitionApplicationCreateView(generics.CreateAPIView):
    queryset = ExhibitionApplication.objects.all()
    serializer_class = ExhibitionApplicationSerializer
    permission_classes = [AllowAny]

    """Function to send mail after a successful registration"""
    def perform_create(self, serializer):
        try:
            application = serializer.save()
            submission_date = now()  # Get current date and time

            # Email to the user (applicant)
            self.send_user_email(application)

            # Email to the admin
            self.send_admin_email(application, submission_date)

        except Exception as e:
            logger.error(f"Error occurred while processing the application: {e}")
            raise  # Re-raise the exception to maintain the API behavior

    def send_user_email(self, application):
        """Send confirmation email to the applicant"""
        try:
            user_subject = 'Application Received'
            user_message = render_to_string('emails/user_application_received.html', {'application': application})
            user_email = application.email
            send_mail(
                subject=user_subject,
                from_email='lastborn.ai@gmail.com',
                recipient_list=[user_email],
                fail_silently=False,
                html_message=user_message,  # Send the HTML version of the email
            )
        except Exception as e:
            logger.error(f"Error sending user email for application {application.id}: {e}")

    def send_admin_email(self, application, submission_date):
        """Send notification email to the admin"""
        try:
            admin_subject = 'New Exhibition Application Submitted'
            admin_message = render_to_string(
                'emails/admin_application_notification.html',
                {'application': application, 'submission_date': submission_date}
            )
            email = EmailMessage(
                subject=admin_subject,
                body=admin_message,
                from_email='lastborn.ai@gmail.com',
                to=['arcademw1@gmail.com'],
            )
            email.send(fail_silently=False)
        except Exception as e:
            logger.error(f"Error sending admin email for application {application.id}: {e}")



# Exhibition application view
# class ExhibitionApplicationCreateView(generics.CreateAPIView):
#     queryset = ExhibitionApplication.objects.all()
#     serializer_class = ExhibitionApplicationSerializer

#     """ Function to send mail after a successful registration """
#     def perform_create(self, serializer):
#         application = serializer.save()
#         submission_date = now()  # Get current date and time

#         # Email to the user (applicant)
#         user_subject = 'Application Received'
#         user_message = render_to_string('emails/user_application_received.html', {'application': application})
#         user_email = application.email
#         send_mail(
#             subject=user_subject,
#             from_email='lastborn.ai@gmail.com',
#             recipient_list=[user_email],
#             fail_silently=False,
#             html_message=user_message  # Send the HTML version of the email
#         )

#         # Prepare email to the admin
#         admin_subject = 'New Exhibition Application Submitted'
#         admin_message = render_to_string('emails/admin_application_notification.html', {'application': application, 'submission_date': submission_date})
#         email = EmailMessage(
#             subject=admin_subject,
#             body=admin_message,
#             from_email='lastborn.ai@gmail.com',
#             to=['arcademw1@gmail.com'],
#         )

#         # Send the email to the admin without the PDF attachment
#         email.send(fail_silently=False)


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

