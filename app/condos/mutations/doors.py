"""Module for grouping Mutations about the state of the door"""
import graphene
from graphql_jwt.decorators import superuser_required
from ..models import Block, Apartment
from ..types import BlockType, ApartmentType
from condos import door

class UpdateDoor(graphene.Mutation):
    """Mutation from graphene for updating the state of the door"""
    enter = graphene.Boolean()

    class Arguments:
        """Mutation arguments for updating blocks"""
        enter = graphene.Boolean(required=True)

    def mutate(self, info, enter):
        """Method to execute the mutation"""
        door.door_instance.value = enter
        return UpdateDoor(enter=enter)
