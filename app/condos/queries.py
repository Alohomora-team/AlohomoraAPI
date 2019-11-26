"""Module for grouping graphQL queries"""
import graphene
from graphql_jwt.decorators import superuser_required
from condos import door
from .models import Block, Apartment
from .types import BlockType, ApartmentType

class Query():
    """Used to read or fetch values"""

    all_blocks = graphene.List(BlockType)
    all_apartments = graphene.List(ApartmentType)
    door = graphene.Boolean()

    apartments = graphene.Field(
        graphene.List(ApartmentType),
        number=graphene.String()
        )

    block = graphene.Field(
        BlockType,
        number=graphene.String()
        )

    apartment = graphene.Field(
        ApartmentType,
        number=graphene.String(),
        block=graphene.String()
        )

    def resolve_door(self, info):
        """Say if the door can be open"""
        return door.door_instance.value

    def resolve_all_blocks(self, info, **kwargs):
        """Returns all Block type objects"""
        return Block.objects.all()

    def resolve_all_apartments(self, info, **kwargs):
        """Returns all Apartment type objects"""
        return Apartment.objects.all()

    def resolve_apartment(self, info, **kwargs):
        """Returns a specific Apartment type object"""
        number = kwargs.get('number')
        block = kwargs.get('block')
        block_obj = Block.objects.get(number=block)

        if number is not None and block_obj is not None:
            return Apartment.objects.get(number=number, block=block_obj)

        return None

    def resolve_block(self, info, **kwargs):
        """Returns a specific Block type object"""
        number = kwargs.get('number')

        if number is not None:
            return Block.objects.get(number=number)

        return None

    def resolve_apartments(self, info, **kwargs):
        """Returns all Apartment type objects that match a number"""
        number = kwargs.get('number')

        if number is not None:
            return Apartment.objects.filter(number=number).all()

        return None
