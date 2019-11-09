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


    # @login_required
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

    #@superuser_required
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

    #@superuser_required
    def mutate(self, info, email, user_email):
        """Method to execute the mutation"""
        user = get_user_model().objects.get(email=user_email)
        user.email = email
        user.save()
        return ChangePassword(user=user)

class ActivateUser(graphene.Mutation):
    """Mutation from graphene for activating user"""
    user = graphene.Field(UserType)

    class Arguments:
        """Mutation arguments for activate a user"""
        user_email = graphene.String()
    def mutate(self, info, user_email):
        """Method to execute the mutation"""
        user = get_user_model().objects.get(email=user_email)
        user.is_active = True
        user.save()
        return ActivateUser(user=user)

class DeactivateUser(graphene.Mutation):
    """Mutation from graphene for deactivating user"""
    user = graphene.Field(UserType)

    class Arguments:
        """Mutation arguments for deactivate a user"""
        user_email = graphene.String()
    def mutate(self, info, user_email):
        """Method to execute the mutation"""
        user = get_user_model().objects.get(email=user_email)
        user.is_active = False
        user.save()
        return ActivateUser(user=user)
