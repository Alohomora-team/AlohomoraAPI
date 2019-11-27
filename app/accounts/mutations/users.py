"""
Mutations that createa a CRUD for normal users
"""
import graphene
from django.contrib.auth import get_user_model
from graphql_jwt.decorators import superuser_required, login_required
from accounts.types import UserType

class CreateUser(graphene.Mutation):
    """Mutation from graphene for creating user"""
    user = graphene.Field(UserType)
    class Arguments:
        """Mutation arguments for create a user"""
        username = graphene.String(required=True)
        password = graphene.String(required=True)
        email = graphene.String(required=True)


    @login_required
    def mutate(self, info, password, username, email):
        """Method to execute the mutation"""
        user = get_user_model()(
            username=username,
            email=email,
        )
        user.set_password(password)
        user.save()

        return CreateUser(user=user)

class ChangePassword(graphene.Mutation):
    """Mutation from graphene for changing password from user"""
    user = graphene.Field(UserType)
    class Arguments:
        """Mutation arguments"""
        password = graphene.String(required=True)
        user_email = graphene.String(required=True)

    @superuser_required
    def mutate(self, info, password, user_email):
        """Method to execute the mutation"""
        user = get_user_model().objects.get(email=user_email)
        user.set_password(password)
        user.save()
        return ChangePassword(user=user)

class ChangeEmail(graphene.Mutation):
    """Mutation from graphene for changing email from user"""
    user = graphene.Field(UserType)
    class Arguments:
        """Mutation arguments"""
        user_email = graphene.String(required=True)
        email = graphene.String(required=True)

    @superuser_required
    def mutate(self, info, email, user_email):
        """Method to execute the mutation"""
        user = get_user_model().objects.get(email=user_email)
        user.email = email
        user.save()
        return ChangePassword(user=user)

class UserActivationManager(graphene.Mutation):
    """Generic classe used to activate/deactivate users"""
    user = graphene.Field(UserType)

    class Arguments:
        """Mutation arguments for activate/deactive a user"""
        user_email = graphene.String()

    @superuser_required
    def mutate(self, info, user_email):
        """Method to execute the mutation"""
        user = get_user_model().objects.get(email=user_email)

        # Decidindo o comportamento da mutation baseada no nome dela ("Polimorfismo")
        if info.field_name == 'activateUser':
            user.is_active = True
        else:
            user.is_active = False

        user.save()

        return UserActivationManager(user=user)


class ActivateUser(UserActivationManager):
    """Mutation from graphene for activating user"""

class DeactivateUser(UserActivationManager):
    """Mutation from graphene for deactivating user"""
