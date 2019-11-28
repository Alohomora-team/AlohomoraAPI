"""
Services queries
"""

import graphene
from graphql_jwt.decorators import superuser_required
from accounts.models import Service
from accounts.types import ServiceType

class ServicesQuery(graphene.AbstractType):
    """Used to read or fetch values"""
    services = graphene.List(ServiceType)

    @superuser_required
    def resolve_services(self, info, **kwargs):
        """Query all services"""
        return Service.objects.all()
