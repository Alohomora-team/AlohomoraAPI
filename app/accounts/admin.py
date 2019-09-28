from django.contrib import admin

from accounts.models import User, Visitor

admin.site.register(User)
admin.site.register(Visitor)

# Register your models here.
