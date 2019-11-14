"""
Mutation that implements a CRUD to services users
"""

import graphene
from django.contrib.auth import get_user_model
from graphql_jwt.decorators import superuser_required, login_required
from accounts.models import Service
from accounts.types import ServiceType, UserType, ServiceInput

class CreateService(graphene.Mutation):
    """Mutation from graphene for creating service"""

    service = graphene.Field(ServiceType)

    class Arguments:
        """Mutation arguments for create a service"""
        password = graphene.String(required=True)
        email = graphene.String(required=True)
        complete_name = graphene.String(required=True)

    # @superuser_required
    def mutate(self, info, **kwargs):
        """Method to execute the mutation"""
        email = kwargs.get('email')
        password = kwargs.get('password')
        complete_name = kwargs.get('complete_name')
        user = get_user_model()(email=email)
        user.set_password(password)
        user.is_service = True
        user.save()
        service = Service.objects.create(user=user)
        service = Service(
            complete_name=complete_name,
            email=email,
            user=user,
        )
        service.save()

        return CreateService(service=service)

class UpdateService(graphene.Mutation):
    """Mutation from graphene for updating service"""
    user = graphene.Field(UserType)
    service = graphene.Field(ServiceType)

    class Arguments:
        """Mutation arguments for update a service"""
        service_data = ServiceInput()

    # @login_required
    def mutate(self, info, service_data=None):
        """Method to execute the mutation"""
        user = info.context.user
        if user.is_service is False:
            raise Exception('User is not service')
        email = user.email
        service = Service.objects.get(email=email)
        for key, value in service_data.items():
            if (key == 'password') and (value is not None):
                user.set_password(service_data.password)
            if (key == 'email') and (value is not None):
                setattr(user, key, value)
            if (key == 'email') and (value is not None):
                setattr(service, key, value)
            else:
                setattr(service, key, value)
        service.save()
        user.save()
        return UpdateService(user=user, service=service)

class DeleteService(graphene.Mutation):
    """Mutation from graphene for deleting service"""
    service_email = graphene.String()

    class Arguments:
        """Mutation arguments for delete aservice"""
        service_email = graphene.String(required=True)

    # @superuser_required
    def mutate(self, info, service_email):
        """Method to execute the mutation"""
        service = Service.objects.get(email=service_email)
        user = get_user_model().objects.get(email=service_email)
        user.delete()
        service.delete()
