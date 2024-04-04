from django.contrib import admin

from .models import User, TemporaryUser

admin.site.register(User)
admin.site.register(TemporaryUser)

