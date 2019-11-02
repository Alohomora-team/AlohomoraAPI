import graphene
from condos.models import Apartment, Block
from condos.types import ApartmentType, BlockType
from django.contrib.auth import get_user_model
from django.utils import timezone
from graphql_jwt.decorators import superuser_required, login_required
from accounts.models import Visitor, Resident, Entry
from accounts.types import ResidentType, VisitorType

class CreateEntry(graphene.Mutation):
    """Mutation from graphene for creating entry"""

    resident = graphene.Field(ResidentType)
    apartment = graphene.Field(ApartmentType)

    resident_cpf = graphene.String()
    apartment_number = graphene.String()

    class Arguments:
        """Mutation arguments for create a entry for a resident"""
        resident_cpf = graphene.String()
        apartment_number = graphene.String()

    def mutate(self, info, resident_cpf, apartment_number):
        """Method to execute the mutation"""
        resident = Resident.objects.filter(cpf=resident_cpf).first()
        apartment = Apartment.objects.filter(number=apartment_number).first()

        entry = Entry(resident=resident, apartment=apartment)
        entry.date = timezone.now()
        entry.save()

        return CreateEntry(resident=entry.resident, apartment=entry.apartment)

class CreateEntryVisitor(graphene.Mutation):
    """Mutation from graphene for creating entries from visitors"""

    visitor = graphene.Field(VisitorType)
    apartment = graphene.Field(ApartmentType)
    pending = graphene.Boolean()

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

        return CreateEntryVisitor(
            visitor=visitor,
            apartment=apartment,
            pending=pending
            )
