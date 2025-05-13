from django.contrib import admin
from django.urls import path, include, re_path
from knox import views as knox_views
from django.conf import settings
from django.conf.urls.static import static

# swagger documentation
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions


# documentation 
schema_view = get_schema_view(
   openapi.Info(
      title="Arcade Dynasty",
      default_version='v1.0.0',
      description="Detailed API documentation Arcade Backend operations",
    #   terms_of_service="https://www.yourwebsite.com/terms/",
      contact=openapi.Contact(email="arcademw1@gmail.com"),
      license=openapi.License(name="MIT License"),
   ),
   public=True,
   permission_classes=[permissions.AllowAny],
)


urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("users.urls")),
    path("api/auth/", include("knox.urls")),
    path("logout/", knox_views.LogoutView.as_view(), name="knox_logout"),
    path("logoutall/", knox_views.LogoutAllView.as_view(), name="knox_logoutall"),
    path(
        "api/password_reset/",
        include("django_rest_passwordreset.urls", namespace="password_reset"),
    ),

    # swagger 
    # re_path(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),   # Documentation & payloads
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

