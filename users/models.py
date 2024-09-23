from django.db import models
from django.db import models
from django.contrib.auth.base_user import BaseUserManager

from django_rest_passwordreset.signals import reset_password_token_created
from django.dispatch import receiver
from django.urls import reverse
from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives
from django.utils.html import strip_tags

from django.contrib.auth.models import AbstractUser, BaseUserManager, Group, Permission
from django.db import models
from django.conf import settings
from django.contrib.auth import get_user_model

# Registration models 
class CustomUserManager(BaseUserManager):
    def create_user(self, username, email, password=None, **extra_fields):
        if not email:
            raise ValueError('Email is a required field')

        email = self.normalize_email(email)
        user = self.model(username=username, email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(username=username, email=email, password=password, **extra_fields)

class CustomUser(AbstractUser):
    username = models.CharField(max_length=200, null=True, blank=True)
    email = models.EmailField(max_length=200, unique=True)
    birthday = models.DateField(null=True, blank=True)

    # Add related_name to avoid clashes with Django's built-in User model
    groups = models.ManyToManyField(
        Group,
        related_name="customuser_set",  # Avoid clashes
        blank=True
    )
    user_permissions = models.ManyToManyField(
        Permission,
        related_name="customuser_permissions_set",  # Avoid clashes
        blank=True
    )

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']


# Password reset model 
@receiver(reset_password_token_created)
def password_reset_token_created(reset_password_token, *args, **kwargs):
    sitelink = "http://localhost:5173/"
    token = "{}".format(reset_password_token.key)
    full_link = str(sitelink) + str("password-reset/") + str(token)

    print(token)
    print(full_link)

    context = {"full_link": full_link, "email_adress": reset_password_token.user.email}

    html_message = render_to_string("emails/password_reset_email.html", context=context)
    plain_message = strip_tags(html_message)

    msg = EmailMultiAlternatives(
        subject="Request for resetting password for {title}".format(
            title=reset_password_token.user.email
        ),
        body=plain_message,
        from_email="sender@example.com",
        to=[reset_password_token.user.email],
    )

    msg.attach_alternative(html_message, "text/html")
    msg.send()


# exhibition 
class ExhibitionApplication(models.Model):
    brand_name = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=15)
    email = models.EmailField()
    country = models.CharField(max_length=50)
    state = models.CharField(max_length=50, blank=True)
    city = models.CharField(max_length=50)
    postal_code = models.CharField(max_length=10)

    application_type = models.JSONField()  # To store multiple choices
    designer_category = models.JSONField()  # To store multiple choices
    submitted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.brand_name
    

# Mustread section model 
class MustRead(models.Model):
    title = models.CharField(max_length=100, blank=False)
    image = models.ImageField(upload_to='Gallery-images/')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
    body = models.TextField(default='Paste', null=True)
    
    def __str__(self):
        return self.title


# Event broadcast 
class UpcomingEvent(models.Model):
    title = models.CharField(max_length=100, blank=False)
    image = models.ImageField(upload_to ='Upcoming_event/')

    def __str__(self):
        return self.title


# Blog post 
class Blog(models.Model):
    title = models.CharField(max_length=100, blank=False)
    image = models.ImageField(upload_to='blog/')
    description = models.CharField(max_length=300)
    body = models.TextField()

    def __str__(self):
        return f"Title of blog - {self.title}"
