"""
User indiviual and ilstings queries
"""

import graphene
from django.contrib.auth import get_user_model
from graphql_jwt.decorators import superuser_required, login_required
from accounts.types import UserType

class UsersQuery(graphene.AbstractType):
    """Used to read or fetch values"""

    users = graphene.List(UserType)
    unactives_users = graphene.List(UserType)
    me = graphene.Field(UserType)

    @superuser_required
    def resolve_unactives_users(self, info, **kwargs):
        """Query all unactives users"""
        return get_user_model().objects.filter(is_active=False)

    @login_required
    def resolve_me(self, info):
        """Search for user features"""
        user = info.context.user
        return user

    @superuser_required
    def resolve_users(self, info, **kwargs):
        """Query all users"""
        return get_user_model().objects.all()
