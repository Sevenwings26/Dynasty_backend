from django.urls import path
from rest_framework.routers import DefaultRouter

from django.urls import path
from .views import *
# GalleryListView, UpcomingEventListView, BlogListView

urlpatterns = [
]

from django.conf import settings
from django.conf.urls.static import static


# Define your router and register viewsets
router = DefaultRouter()
router.register("register", RegisterViewset, basename="register")
router.register("login", LoginViewset, basename="login")

# Define the additional URL patterns
urlpatterns = [
    # registration form 

    path('register-designer/', DesignerRegistrationCreateView.as_view(), name='designer-registration'),
    # api get 
    path('api/gallery/', MustReadListView.as_view(), name='gallery-list'),
    path('api/upcoming-events/', UpcomingEventListView.as_view(), name='upcoming-event-list'),
    path('api/blogs/', BlogListView.as_view(), name='blog-list'),
    path('user/', UserDetailView.as_view(), name='user-detail'),
]


urlpatterns += router.urls

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

