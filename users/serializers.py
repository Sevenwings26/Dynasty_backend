from rest_framework import serializers 
from .models import * 
from django.contrib.auth import get_user_model

User = get_user_model()

class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()

    def to_representation(self, instance):
        ret = super().to_representation(instance)
        ret.pop('password', None)
        return ret

class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ('id', 'username', 'email', 'password')
        extra_kwargs = {
            'password': {'write_only': True}
        }
    
    def create(self, validated_data):
        email = validated_data.get('email')
        if CustomUser.objects.filter(email=email).exists():
            raise serializers.ValidationError({"email": "This email address is already in use."})

        user = CustomUser.objects.create_user(**validated_data)
        return user


class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'email', 'birthday']


class ApplicationTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ApplicationType
        fields = ['id', 'name']

class DesignerCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = DesignerCategory
        fields = ['id', 'name']

class DesignerRegistrationSerializer(serializers.ModelSerializer):
    # Accepting list of IDs instead of nested serializers
    application_type = serializers.PrimaryKeyRelatedField(queryset=ApplicationType.objects.all(), many=True)
    designer_category = serializers.PrimaryKeyRelatedField(queryset=DesignerCategory.objects.all(), many=True)

    class Meta:
        model = DesignerRegistration
        fields = [
            'id', 'brand_name', 'email', 'phone_number', 'country', 
            'state', 'city', 'postal_code', 'application_type', 'designer_category'
        ]

    def create(self, validated_data):
        # Pop the many-to-many related fields
        application_types = validated_data.pop('application_type')
        designer_categories = validated_data.pop('designer_category')
        
        # Create the DesignerRegistration instance
        designer_registration = DesignerRegistration.objects.create(**validated_data)
        
        # Add the application types and designer categories
        designer_registration.application_type.set(application_types)
        designer_registration.designer_category.set(designer_categories)
        
        return designer_registration



class MustReadSerializer(serializers.ModelSerializer):
    class Meta:
        model = MustRead
        fields = '__all__'

class UpcomingEventSerializer(serializers.ModelSerializer):
    class Meta:
        model = UpcomingEvent
        fields = '__all__'

class BlogSerializer(serializers.ModelSerializer):
    class Meta:
        model = Blog
        fields = '__all__'

