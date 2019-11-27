"""Module for grouping Mutations about entries from a visitor"""
import graphene
from django.contrib.auth import get_user_model
from condos.models import Apartment, Block
from condos.types import ApartmentType, BlockType
from graphql_jwt.decorators import superuser_required, login_required
from accounts.models import Visitor, EntryVisitor
from accounts.types import EntryVisitorType

class CreateEntryVisitor(graphene.Mutation):
    """Mutation from graphene for creating entries from visitors"""

    entry_visitor = graphene.Field(EntryVisitorType)

    class Arguments:
        """Mutation arguments for create a entry for a visitor"""
        visitor_cpf = graphene.String()
        block_number = graphene.String()
        apartment_number = graphene.String()

    @superuser_required
    def mutate(self, info, **kwargs):
        """Method to execute the mutation"""
        visitor_cpf = kwargs.get('visitor_cpf')
        block_number = kwargs.get('block_number')
        apartment_number = kwargs.get('apartment_number')

        visitor = Visitor.objects.get(cpf=visitor_cpf)

        if visitor is None:
            raise Exception('Visitor not found')

        block = Block.objects.get(number=block_number)

        if block is None:
            raise Exception('Block not found')

        apartment = Apartment.objects.get(
                block=block,
                number=apartment_number
                )

        if apartment is None:
            raise Exception('Apartment not found')

        entry = EntryVisitor(
                visitor=visitor,
                apartment=apartment,
                )

        entry.save()

        return CreateEntryVisitor(entry_visitor=entry)
