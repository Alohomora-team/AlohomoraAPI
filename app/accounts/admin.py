from django.contrib import admin

from accounts.models import User, Visitor, Service

admin.site.register(User)
admin.site.register(Service)
admin.site.register(Visitor)
