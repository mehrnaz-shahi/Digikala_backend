from django.contrib import admin

from .models import TemporaryUser

from django.contrib.auth import get_user_model

User = get_user_model()


class UserAdmin(admin.ModelAdmin):
    list_display = ["phone_number", "id"]


admin.site.register(User, UserAdmin)

admin.site.register(TemporaryUser)
