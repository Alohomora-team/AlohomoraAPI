import graphene
from graphql_jwt.decorators import superuser_required
from .models import Block, Apartment
from .types import BlockType, ApartmentType

class Query():
    """Used to read or fetch values"""

    all_blocks = graphene.List(BlockType)
    all_apartments = graphene.List(ApartmentType)

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

    def resolve_all_blocks(self, info, **kwargs):
        return Block.objects.all()

    def resolve_all_apartments(self, info, **kwargs):
        return Apartment.objects.all()

    def resolve_apartment(self, info, **kwargs):
        number = kwargs.get('number')
        block = kwargs.get('block')
        block_obj = Block.objects.get(number=block)

        if number is not None and block_obj is not None:
            return Apartment.objects.get(number=number, block=block_obj)

        return None

    def resolve_block(self, info, **kwargs):
        number = kwargs.get('number')

        if number is not None:
            return Block.objects.get(number=number)

        return None

    def resolve_apartments(self, info, **kwargs):
        number = kwargs.get('number')

        if number is not None:
            return Apartment.objects.filter(number=number).all()

        return None