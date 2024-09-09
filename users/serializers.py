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


class ApplicationTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ApplicationType
        fields = ['id', 'name']

class DesignerCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = DesignerCategory
        fields = ['id', 'name']

class DesignerRegistrationSerializer(serializers.ModelSerializer):
    application_type = ApplicationTypeSerializer(many=True)
    designer_category = DesignerCategorySerializer(many=True)

    class Meta:
        model = DesignerRegistration
        fields = ['id', 'brand_name', 'email', 'phone_number', 'country', 'state', 'city', 'postal_code', 'application_type', 'designer_category']

    def create(self, validated_data):
        application_types_data = validated_data.pop('application_type')
        designer_categories_data = validated_data.pop('designer_category')

        designer_registration = DesignerRegistration.objects.create(**validated_data)
        for app_type_data in application_types_data:
            app_type, created = ApplicationType.objects.get_or_create(**app_type_data)
            designer_registration.application_type.add(app_type)
        for cat_data in designer_categories_data:
            cat, created = DesignerCategory.objects.get_or_create(**cat_data)
            designer_registration.designer_category.add(cat)

        return designer_registration


# class DesignerRegistrationSerializer(serializers.ModelSerializer):
#     application_type = serializers.PrimaryKeyRelatedField(queryset=ApplicationType.objects.all(), many=True)
#     designer_category = serializers.PrimaryKeyRelatedField(queryset=DesignerCategory.objects.all(), many=True)

#     class Meta:
#         model = DesignerRegistration
#         fields = ['id', 'brand_name', 'email', 'phone_number', 'country', 'state', 'city', 'postal_code', 'application_type', 'designer_category']

#     def create(self, validated_data):
#         application_types = validated_data.pop('application_type')
#         designer_categories = validated_data.pop('designer_category')

#         designer_registration = DesignerRegistration.objects.create(**validated_data)
#         designer_registration.application_type.set(application_types)
#         designer_registration.designer_category.set(designer_categories)

#         return designer_registration


class GallerySerializer(serializers.ModelSerializer):
    image = serializers.ImageField()
    class Meta:
        model = Gallery
        fields = ('title','image')


# class UpcomingEventSerializer(serializers.ModelSerializer):
#     image = serializers.ImageField()
#     class Meta:
#         model = UpcomingEvent
#         fields = ('title', 'image')


# class BlogSerializer(serializers.ModelSerializer):
#     image = serializers.SerializerMethodField()

#     def get_image(self, obj):
#         request = self.context.get('request')
#         if request:
#             return request.build_absolute_uri(obj.image.url)
#         else:
#             return obj.image.url

#     class Meta:
#         model = Blog
#         fields = ('title', 'image', 'description', 'body')

class BlogSerializer(serializers.ModelSerializer):
    image = serializers.ImageField()
    class Meta:
        model = Blog
        fields = ('title','image','description','body')
