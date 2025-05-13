from django.shortcuts import render
from django_q.tasks import async_task
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

def send_welcome_email(user):
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
    email.content_subtype = "html"
    email.send(fail_silently=True)

# import logging

# logger = logging.getLogger(__name__)

# def send_welcome_email(user_id, username, email):
#     try:
#         context = {'first_name': username}
#         html_message = render_to_string('emails/welcome_email_template.html', context)

#         subject = "Welcome to Our Platform"
#         email_msg = EmailMessage(
#             subject=subject,
#             body=html_message,
#             from_email='arcademw1@gmail.com',
#             to=[email],
#         )
#         email_msg.content_subtype = "html"
#         email_msg.send()
#         logger.info(f"Welcome email sent to {email}")
#     except Exception as e:
#         logger.error(f"Failed to send welcome email to {email}: {e}")



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
            #  Send Email Asynchronously in background thread.
            threading.Thread(target=send_welcome_email, args=(user,)).start()
            # async_task('send_welcome_email', user_id=user.id, username=user.username, email=user.email)
            return Response({"message": "Registration successful! A welcome email has been sent."}, status=201)
        else:
            return Response(serializer.errors, status=400)
