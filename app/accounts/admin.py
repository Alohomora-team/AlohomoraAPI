"""
Adding accounts models in django admin site
"""

from django.contrib import admin
from accounts.models import User, Visitor, Service, Resident, EntryVisitor

admin.site.register(User)
admin.site.register(Service)
admin.site.register(Visitor)
admin.site.register(Resident)
admin.site.register(EntryVisitor)
