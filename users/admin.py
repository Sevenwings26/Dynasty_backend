from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(CustomUser)

# @admin.register(DesignerRegistration)
# class DesignerRegistrationAdmin(admin.ModelAdmin):
# #     list_display = [
# #         'brand_name', 'email', 'city', 'phone_number'
#     # ]
#     pass

admin.site.register(MustRead)
# admin.site.register(Gallery)
admin.site.register(Blog)
admin.site.register(UpcomingEvent)
admin.site.register(ExhibitionApplication)


# admin.site.register(Designer)
# admin.site.register(ApplicationType)
# admin.site.register(DesignerCategory)
# admin.site.register(DesignerRegistration)


