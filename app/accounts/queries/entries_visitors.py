"""
Resolve data about visitos entries
"""
import graphene
from condos.models import Apartment, Block
from accounts.models import Visitor, EntryVisitor
from accounts.types import EntryVisitorType

class EntriesVisitorsQuery(graphene.AbstractType):
    """Fetch data about entries of visitos in a apartment"""
    all_entries_visitors = graphene.List(EntryVisitorType)

    entries_visitor = graphene.Field(
        graphene.List(EntryVisitorType),
        cpf=graphene.String(),
        block_number=graphene.String(),
        apartment_number=graphene.String(),
        )

    entries_visitors_pending = graphene.Field(
        graphene.List(EntryVisitorType),
        apartment_id=graphene.String(),
        )

    def resolve_all_entries_visitors(self, info, **kwargs):
        """Query all entries from visitors"""
        return EntryVisitor.objects.all()

    def resolve_entries_visitor(self, info, **kwargs):
        """Query all entries from a specific visitor"""
        cpf = kwargs.get('cpf')
        block_number = kwargs.get('block_number')
        apartment_number = kwargs.get('apartment_number')

        if cpf and block_number and apartment_number:
            visitor = Visitor.objects.get(cpf=cpf)
            block = Block.objects.get(number=block_number)
            apartment = Apartment.objects.get(
                    block=block,
                    number=apartment_number
                    )

            return EntryVisitor.objects.filter(
                    apartment=apartment,
                    visitor=visitor
                    )

        if block_number and apartment_number:
            block = Block.objects.get(number=block_number)
            apartment = Apartment.objects.get(
                    block=block,
                    number=apartment_number
                    )

            return EntryVisitor.objects.filter(apartment=apartment)

        if cpf:
            visitor = Visitor.objects.get(cpf=cpf)
            return EntryVisitor.objects.filter(visitor=visitor)


        return None

    def resolve_entries_visitors_pending(self, info, **kwargs):
        """Query all pending entries to a specific apartment"""
        apartment_id = kwargs.get('apartment_id')

        #Lista entradas pendentes de um apartamento de determinado bloco
        if apartment_id:

            return EntryVisitor.objects.filter(
                pending=True,
                apartment_id=apartment_id
                )

        return None
