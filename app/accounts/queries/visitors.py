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

class VisitorsQuery(graphene.AbstractType):
    """Used to read or fetch values"""

    all_visitors = graphene.List(VisitorType)


    visitor = graphene.Field(
        VisitorType,
        cpf=graphene.String()
        )

    @superuser_required
    def resolve_all_visitors(self, info, **kwargs):
        """Query all visitors"""
        return Visitor.objects.all()

    @superuser_required
    def resolve_visitor(self, info, **kwargs):
        """Query a specific visitor"""
        cpf = kwargs.get('cpf')

        return Visitor.objects.get(cpf=cpf)
