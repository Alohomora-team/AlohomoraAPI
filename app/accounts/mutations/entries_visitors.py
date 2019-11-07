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
        pending = graphene.Boolean()

    def mutate(self, info, **kwargs):
        """Method to execute the mutation"""
        visitor_cpf = kwargs.get('visitor_cpf')
        block_number = kwargs.get('block_number')
        apartment_number = kwargs.get('apartment_number')
        pending = kwargs.get('pending')

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
                pending=pending
                )

        entry.save()

        return CreateEntryVisitor(entry_visitor=entry)

# allow visitor entry
class UpdateEntryVisitorPending(graphene.Mutation):

    entry_id = graphene.String()
    entry_visitor_pending = graphene.Boolean()

    class Arguments:
        entry_id = graphene.String()

    def mutate(self, info, **kwargs):
        entry_id = kwargs.get('entry_id')

        entry = EntryVisitor.objects.get(id=entry_id)

        entry.pending = False

        entry.save()

        return UpdateEntryVisitorPending(
            entry_id=entry.id,
            entry_visitor_pending=entry.pending
            )

class DeleteEntryVisitorPending(graphene.Mutation):
    """Mutation from graphene for deleting visitor"""

    deleted = graphene.Boolean()

    class Arguments:
        """Mutation arguments for delete a visitor"""
        entry_id = graphene.String(required=True)

    def mutate(self, info, **kwargs):
        """Method to execute the mutation"""
        entry_id = kwargs.get('entry_id')

        entry_visitor = EntryVisitor.objects.get(id=entry_id)
        entry_visitor.delete()

        return DeleteEntryVisitorPending(deleted=True)

class DeleteEntriesVisitorsPending(graphene.Mutation):
    """Mutation from graphene for deleting visitor"""

    deleted = graphene.Boolean()

    class Arguments:
        """Mutation arguments for delete a visitor"""
        apartment_id = graphene.String(required=True)

    def mutate(self, info, **kwargs):
        """Method to execute the mutation"""
        apartment_id = kwargs.get('apartment_id')

        entry_visitors = EntryVisitor.objects.all().filter(apartment_id=apartment_id)
        entry_visitors.delete()

        return DeleteEntriesVisitorsPending(deleted=True)
