"""Module for grouping Mutations about Apartments"""
import graphene
from graphql_jwt.decorators import superuser_required
from ..models import Block, Apartment
from ..types import BlockType, ApartmentType

class CreateBlock(graphene.Mutation):
    """Mutation from graphene for creating blocks"""

    number = graphene.String()
    class Arguments:
        """Mutation arguments for creating blocks"""
        number = graphene.String()

    @superuser_required
    def mutate(self, info, number):
        """Method to execute the mutation"""
        block = Block(number=number)
        block.save()

        return CreateBlock(
            number=block.number)


class UpdateBlock(graphene.Mutation):
    """Mutation from graphene for updating blocks"""
    block = graphene.Field(BlockType)
    number = graphene.String()
    block_number = graphene.String()

    class Arguments:
        """Mutation arguments for updating blocks"""
        number = graphene.String(required=True)
        block_number = graphene.String(required=True)

    def mutate(self, info, number, block_number):
        """Method to execute the mutation"""
        block = Block.objects.get(number=block_number)
        block.number = number
        block.save()
        return UpdateBlock(block=block)


class DeleteBlock(graphene.Mutation):
    """Mutation from graphene for deleting blocks"""
    block_number = graphene.String()

    class Arguments:
        """Mutation arguments for deleting blocks"""
        block_number = graphene.String(required=True)

    def mutate(self, info, block_number):
        """Method to execute the mutation"""
        block = Block.objects.get(number=block_number)
        block.delete()
