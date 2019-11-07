import graphene
from graphql_jwt.decorators import superuser_required
from ..models import Block, Apartment
from ..types import BlockType, ApartmentType

class CreateBlock(graphene.Mutation):
    """Mutation from graphene for creating block"""

    number = graphene.String()
    class Arguments:
        number = graphene.String()

    @superuser_required
    def mutate(self, info, number):
        block = Block(number=number)
        block.save()

        return CreateBlock(
            number=block.number)


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


class DeleteBlock(graphene.Mutation):
    block_number = graphene.String()

    class Arguments:
        block_number = graphene.String(required=True)

    def mutate(self, info, block_number):
        block = Block.objects.get(number=block_number)
        block.delete()
