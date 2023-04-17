from django.contrib import admin

from authentication.models import User, Profile, Address, BusinessInfo, UserToken, Reset
# Register your models here.
admin.site.register(User)
admin.site.register(Profile)
admin.site.register(Address)
admin.site.register(BusinessInfo)
admin.site.register(UserToken)
admin.site.register(Reset)
