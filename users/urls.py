from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import (
    DesignerRegistrationCreateView,
    ApplicationTypeViewSet,
    DesignerCategoryViewSet,
    LoginViewset,
    UserViewset,
    RegisterViewset,
    galleryViews,
    blog_section,
)

# Define your router and register viewsets
router = DefaultRouter()
router.register("register", RegisterViewset, basename="register")
router.register("login", LoginViewset, basename="login")
router.register("users", UserViewset, basename="users")

# Define the additional URL patterns
urlpatterns = [
    # registration form 
    path('api/register-designer/', DesignerRegistrationCreateView.as_view(), name='register_designer'),
    path('api/application-types/', ApplicationTypeViewSet.as_view({'get': 'list'}), name='application_types'),
    path('api/designer-categories/', DesignerCategoryViewSet.as_view({'get': 'list'}), name='designer_categories'),

    # api get 
    path('api/gallery-views/', galleryViews, name='gallery' ),
    path('api/blog/', blog_section, name='blog' ),
]


urlpatterns += router.urls

