"""
Creates a CRUD to visitors
"""

import graphene
from graphql_jwt.decorators import superuser_required, login_required
from accounts.models import Visitor
from accounts.types import VisitorType

class CreateVisitor(graphene.Mutation):
    """Mutation from graphene for creating visitor"""
    visitor = graphene.Field(VisitorType)


    class Arguments:
        """Mutation arguments for create a visitor"""
        complete_name = graphene.String()
        cpf = graphene.String()

    @superuser_required
    def mutate(self, info, **kwargs):
        """Method to execute the mutation"""
        complete_name = kwargs.get('complete_name')
        cpf = kwargs.get('cpf')

        visitor = Visitor(
            complete_name=complete_name,
            cpf=cpf
        )

        visitor.save()

        return CreateVisitor(visitor=visitor)

class UpdateVisitor(graphene.Mutation):
    """Mutation from graphene for updating visitor"""
    visitor = graphene.Field(VisitorType)

    class Arguments:
        """Mutation arguments for update a visitor"""
        complete_name = graphene.String()
        cpf = graphene.String(required=True)
        new_cpf = graphene.String()

    @superuser_required
    def mutate(self, info, **kwargs):
        """Method to execute the mutation"""
        complete_name = kwargs.get('complete_name')
        cpf = kwargs.get('cpf')
        new_cpf = kwargs.get('new_cpf')

        visitor = Visitor.objects.get(cpf=cpf)

        if new_cpf:
            visitor.cpf = new_cpf

        if complete_name:
            visitor.complete_name = complete_name

        visitor.save()

        return UpdateVisitor(visitor=visitor)

class DeleteVisitor(graphene.Mutation):
    """Mutation from graphene for deleting visitor"""
    cpf = graphene.String()

    class Arguments:
        """Mutation arguments for delete a visitor"""
        cpf = graphene.String(required=True)

    @superuser_required
    def mutate(self, info, cpf):
        """Method to execute the mutation"""
        visitor = Visitor.objects.get(cpf=cpf)
        visitor.delete()

        return DeleteVisitor(
                cpf=cpf
                )
