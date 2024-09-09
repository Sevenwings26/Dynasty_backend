from django.contrib import admin
# from .models import CustomUser, DesignerRegistration
from .models import *

# Register your models here.
admin.site.register(CustomUser)

@admin.register(DesignerRegistration)
class DesignerRegistrationAdmin(admin.ModelAdmin):
    list_display = [
        'brand_name', 'email', 'city', 'phone_number'
    ]

admin.site.register(Gallery)
admin.site.register(Blog)
admin.site.register(UpcomingEvent)

