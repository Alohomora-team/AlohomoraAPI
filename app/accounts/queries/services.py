import graphene
from condos.models import Apartment, Block
from django.contrib.auth import get_user_model
from graphql_jwt.decorators import superuser_required, login_required
from accounts.models import Visitor, Resident, Service, EntryVisitor, Entry, Admin
import accounts.utility as Utility
from accounts.types import (ResidentType,
                             ServiceType,
                             VisitorType,
                             UserType,
                             EntryType,
                             AdminType,
                             EntryVisitorType,)

class ServicesQuery(graphene.AbstractType):
    """Used to read or fetch values"""
    services = graphene.List(ServiceType)
    @superuser_required
    def resolve_services(self, info, **kwargs):
        """Query all services"""
        return Service.objects.all()
