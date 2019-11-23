"""
Mutation for register a entrie
"""

import graphene
from django.contrib.auth import get_user_model
from condos.models import Apartment, Block
from condos.types import ApartmentType, BlockType
from graphql_jwt.decorators import superuser_required, login_required
from accounts.models import Resident, Entry
from accounts.types import ResidentType

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
        entry.save()

        return CreateEntry(resident=entry.resident, apartment=entry.apartment)
