import graphene
from graphql_jwt.decorators import superuser_required
from ..models import Block, Apartment
from ..types import BlockType, ApartmentType

class CreateApartment(graphene.Mutation):
    """Mutation from graphene for creating apartment"""

    number = graphene.String()
    block_number = graphene.String()
    block = graphene.Field(BlockType)

    class Arguments:
        """Mutation arguments for creating apartments"""
        number = graphene.String()
        block_number = graphene.String()

    @superuser_required
    def mutate(self, info, number, block_number):
        """Method to execute the mutation"""
        block = Block.objects.filter(number=block_number).first()
        apartment = Apartment(number=number, block=block)

        if block is None:
            raise Exception('Block not found')


        apartment = Apartment(number=number, block=block)
        apartment.save()

        return CreateApartment(
            number=apartment.number,
            block=apartment.block)

class UpdateApartment(graphene.Mutation):
     """Mutation from graphene for updating apartment"""
    apartment = graphene.Field(ApartmentType)
    number = graphene.String()
    apartment_number = graphene.String()

    class Arguments:
        """Mutation arguments for updating apartments"""
        number = graphene.String(required=True)
        apartment_number = graphene.String(required=True)

    def mutate(self, info, number, apartment_number):
        """Method to execute the mutation"""
        apartment = Apartment.objects.get(number=apartment_number)
        apartment.number = number
        apartment.save()
        return UpdateApartment(apartment=apartment)

class DeleteApartment(graphene.Mutation):
     """Mutation from graphene for deleting apartment"""
    apartment_number = graphene.Int()

    class Arguments:
        """Mutation arguments for deleting apartments"""
        apartment_number = graphene.Int(required=True)

    @superuser_required
    def mutate(self, info, apartment_number):
        """Method to execute the mutation"""
        apartment = Apartment.objects.get(number=apartment_number)
        apartment.delete()
