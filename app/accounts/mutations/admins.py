"""
Create a CRUD of admin users
"""

import graphene
from django.contrib.auth import get_user_model
from graphql_jwt.decorators import superuser_required, login_required
from accounts.models import Admin
from accounts.types import UserType

class CreateAdmin(graphene.Mutation):
    """Mutation from graphene for creating admin"""
    email = graphene.String()
    creator = graphene.Field(UserType)

    class Arguments:
        """Mutation arguments for create a admin"""
        email = graphene.String()
        password = graphene.String()

    @superuser_required
    def mutate(self, info, email, password):
        """Method to execute the mutation"""
        admin = get_user_model().objects.create_superuser(
            email=email,
            password=password,
        )

        admin.set_password(password)
        admin.save()

        creator = info.context.user

        management = Admin(
                admin=admin,
                creator=creator
                )

        management.save()

        return CreateAdmin(
            email=email,
            creator=creator
            )

class DeleteAdmin(graphene.Mutation):
    """Mutation from graphene for deleting admin"""
    email = graphene.String()

    class Arguments:
        """Mutation arguments for delete a admin"""
        email = graphene.String(required=True)

    @superuser_required
    def mutate(self, info, email):
        """Method to execute the mutation"""
        user = info.context.user
        admin = get_user_model().objects.get(email=email)
        creator = Admin.objects.filter(admin=admin).first()

        if creator:
            creator = creator.creator

        if user != admin and user != creator:
            raise Exception('Logged in user is not related')

        admin.delete()

        return DeleteAdmin(
                email=email
                )
