from django.contrib import admin
from basic_app.models import UserProfileInfo, User,userInfo,ms_code_updater

# Register your models here.
admin.site.register(UserProfileInfo)
admin.site.register(userInfo)
admin.site.register(ms_code_updater)
