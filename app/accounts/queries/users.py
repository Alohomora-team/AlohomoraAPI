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

class UsersQuery(graphene.AbstractType):
    """Used to read or fetch values"""

    users = graphene.List(UserType)
    unactives_users = graphene.List(UserType)
    me = graphene.Field(UserType)

    def resolve_unactives_users(self, info, **kwargs):
        """Query all unactives users"""
        return get_user_model().objects.filter(is_active=False)

    def resolve_me(self, info):
        """Search for user features"""
        user = info.context.user
        if user.is_active is False:
            raise Exception('User is NOT active')
        if user.is_service is True:
            raise Exception('User is service')
        if user.is_visitor is True:
            raise Exception('User is visitor')
        if user.is_resident is True:
            raise Exception('User is resident')
        return user

    @superuser_required
    def resolve_users(self, info, **kwargs):
        """Query all users"""
        return get_user_model().objects.all()
