import graphene

from graphene_django.types import DjangoObjectType
from graphql_jwt.decorators import superuser_required

from condos.models import Block, Apartment

class BlockType(DjangoObjectType):
    class Meta:
        model = Block

class ApartmentType(DjangoObjectType):
    class Meta:
        model = Apartment

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

class CreateApartment(graphene.Mutation):
    """Mutation from graphene for creating apartment"""

    number = graphene.String()
    block_number = graphene.String()
    block = graphene.Field(BlockType)

    class Arguments:
        number = graphene.String()
        block_number = graphene.String()

    def mutate(self, info, number, block_number):
        block = Block.objects.filter(number=block_number).first()
        if block is None:
            raise Exception('Block not found')

        apartment = Apartment(number=number, block=block)
        apartment.save()

        return CreateApartment(
            number=apartment.number,
            block=apartment.block)

class CreateBlock(graphene.Mutation):
    """Mutation from graphene for creating block"""

    number = graphene.String()
    class Arguments:
        number = graphene.String()

    def mutate(self, info, number):
        block = Block(number=number, number_id=number)
        block.save()

        return CreateBlock(
            number=block.number)

class DeleteApartment(graphene.Mutation):
    apartment_number = graphene.Int()

    class Arguments:
        apartment_number = graphene.Int(required=True)

    @superuser_required
    def mutate(self, info, apartment_number):
        apartment = Apartment.objects.get(number=apartment_number)
        apartment.delete()

class DeleteBlock(graphene.Mutation):
    block_number = graphene.String()

    class Arguments:
        block_number = graphene.String(required=True)

    def mutate(self, info, block_number):
        block = Block.objects.get(number=block_number)
        block.delete()

class UpdateBlock(graphene.Mutation):
    block = graphene.Field(BlockType)
    number = graphene.String()
    block_number = graphene.String()

    class Arguments:
        number = graphene.String(required=True)
        block_number = graphene.String(required=True)

    def mutate(self, info, number, block_number):
        block = Block.objects.get(number=block_number)
        block.number = number
        block.save()
        return UpdateBlock(block=block)

class UpdateApartment(graphene.Mutation):
    apartment = graphene.Field(ApartmentType)
    number = graphene.String()
    apartment_number = graphene.String()

    class Arguments:
        number = graphene.String(required=True)
        apartment_number = graphene.String(required=True)

    def mutate(self, info, number, apartment_number):
        apartment = Apartment.objects.get(number=apartment_number)
        apartment.number = number
        apartment.save()
        return UpdateApartment(apartment=apartment)


class Mutation(graphene.ObjectType):
    create_apartment = CreateApartment.Field()
    create_block = CreateBlock.Field()
    delete_block = DeleteBlock.Field()
    delete_apartment = DeleteApartment.Field()
    update_block = UpdateBlock.Field()
    update_apartment = UpdateApartment.Field()
