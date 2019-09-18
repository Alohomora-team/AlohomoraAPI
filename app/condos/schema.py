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

    def resolve_all_blocks(self, info, **kwargs):
        return Block.objects.all()

    def resolve_all_apartments(self, info, **kwargs):
        return Apartment.objects.select_related('block').all()


# Mutations

class CreateApartment(graphene.Mutation):
    id = graphene.Int()
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
            id=apartment.id,
            number=apartment.number,
            block=apartment.block)

class CreateBlock(graphene.Mutation):
    id = graphene.Int()
    number = graphene.String()

    class Arguments:
        number = graphene.String()

    def mutate(self, info, number):

        block = Block(number=number)
        block.save()

        return CreateBlock(
            id=block.id,
            number=block.number)



class Mutation(graphene.ObjectType):
    create_apartment = CreateApartment.Field()
    create_block = CreateBlock.Field()
