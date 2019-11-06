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

class EntriesQuery(graphene.AbstractType):
    """Used to read or fetch values"""
    all_entries_visitors = graphene.List(EntryVisitorType)
    entries = graphene.List(EntryType)

    entries_visitor = graphene.Field(
        graphene.List(EntryVisitorType),
        cpf=graphene.String(),
        block_number=graphene.String(),
        apartment_number=graphene.String(),
        )
    entries_visitors_pending = graphene.Field(
        graphene.List(EntryVisitorType),
        block_number=graphene.String(),
        apartment_number=graphene.String(),
        )

    def resolve_all_entries_visitors(self, info, **kwargs):
        """Query all entries from visitors"""
        return EntryVisitor.objects.all()

    def resolve_entries(self, info, **kwargs):
        """Query all entries from residents"""
        return Entry.objects.all()

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
        block_number = kwargs.get('block_number')
        apartment_number = kwargs.get('apartment_number')

        #Lista entradas pendentes de um apartamento de determinado bloco
        if block_number and apartment_number:
            block = Block.objects.get(number=block_number)

            apartment = Apartment.objects.get(
                    block=block,
                    number=apartment_number
                    )

            return EntryVisitor.objects.filter(
                pending=True,
                apartment=apartment
                )

        return None
