import graphene

from graphene_django.types import DjangoObjectType

from condos.models import Block, Apartment

class BlockType(DjangoObjectType):
    class Meta:
        model = Block

class ApartmentType(DjangoObjectType):
    class Meta:
        model = Apartment

class Query():
    all_blocks = graphene.List(BlockType)
    all_apartments = graphene.List(ApartmentType)

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


# Mutations

class CreateApartment(graphene.Mutation):
    number = graphene.String()
    block_number = graphene.String()
    block = graphene.Field(BlockType)

    class Arguments:
        number = graphene.String()
        block_number = graphene.String()


    def mutate(self, info, number, block_number):
        block = Block.objects.filter(number=block_number).first()

        apartment = Apartment(number=number, block=block)
        apartment.save()

        return CreateApartment(
            number=apartment.number,
            block=apartment.block)

class CreateBlock(graphene.Mutation):
    number = graphene.String()

    class Arguments:
        number = graphene.String()

    def mutate(self, info, number):
        block = Block(number=number)
        block.save()

        return CreateBlock(
            number=block.number)



class Mutation(graphene.ObjectType):
    create_apartment = CreateApartment.Field()
    create_block = CreateBlock.Field()
