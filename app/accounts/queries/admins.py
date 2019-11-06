import graphene
from django.contrib.auth import get_user_model
from graphql_jwt.decorators import superuser_required
from accounts.models import Admin
from accounts.types import AdminType

class AdminsQuery(graphene.AbstractType):
    """Used to read or fetch values"""

    all_admins = graphene.List(AdminType)


    admin = graphene.Field(
        graphene.List(AdminType),
        creator_email=graphene.String(),
        admin_email=graphene.String()
        )
    @superuser_required
    def resolve_all_admins(self, info, **kwargs):
        """Query all admins"""
        return Admin.objects.all()

    @superuser_required
    def resolve_admin(self, info, **kwargs):
        """Query a specific admin"""
        creator_email = kwargs.get('creator_email')
        admin_email = kwargs.get('admin_email')

        admin = get_user_model().objects.filter(email=admin_email).first()
        creator = get_user_model().objects.filter(email=creator_email).first()

        if creator_email and admin_email:
            return Admin.objects.filter(
                    creator=creator,
                    admin=admin
                    )

        if creator_email:
            return Admin.objects.filter(
                    creator=creator
                    )

        if admin_email:
            return Admin.objects.filter(
                    admin=admin
                    )
