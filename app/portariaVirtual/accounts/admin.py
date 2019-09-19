from django.contrib import admin

from portariaVirtual.accounts.models import User, Visitor

admin.site.register(User)
admin.site.register(Visitor)

# Register your models here.
