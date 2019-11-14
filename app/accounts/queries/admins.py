"""
Queries that list admin and resolve them individually
"""

import graphene
from django.contrib.auth import get_user_model
from graphql_jwt.decorators import superuser_required
from accounts.models import Admin
from accounts.types import AdminType

class AdminsQuery(graphene.AbstractType):
    """Used to read or fetch values"""

    all_admins = graphene.List(AdminType)

    admin = graphene.Field(
        AdminType,
        admin_email=graphene.String()
        )

    admins = graphene.Field(
        graphene.List(AdminType),
        creator_email=graphene.String()
        )

    # @superuser_required
    def resolve_all_admins(self, info, **kwargs):
        """Query all admins"""
        return Admin.objects.all()

    # @superuser_required
    def resolve_admin(self, info, **kwargs):
        """Query a specific admin"""
        admin_email = kwargs.get('admin_email')

        admin = get_user_model().objects.get(email=admin_email)

        return Admin.objects.get(
                admin=admin
                )

    # @superuser_required
    def resolve_admins(self, info, **kwargs):
        """Query all admins from a creator admin"""
        creator_email = kwargs.get('creator_email')

        creator = get_user_model().objects.get(email=creator_email)

        return Admin.objects.filter(
                creator=creator
                )
