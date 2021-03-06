"""
Bind Apartaments and block mutation to condo mutation
"""

import graphene
from .mutations.apartments import(
    CreateApartment,
    DeleteApartment,
    UpdateApartment,)
from .mutations.blocks import(
    CreateBlock,
    DeleteBlock,
    UpdateBlock,)
from .mutations.doors import UpdateDoor

class Mutation(graphene.ObjectType):
    """
    Create and delete blocks and apartments
    """
    create_apartment = CreateApartment.Field()
    create_block = CreateBlock.Field()
    delete_block = DeleteBlock.Field()
    delete_apartment = DeleteApartment.Field()
    update_block = UpdateBlock.Field()
    update_apartment = UpdateApartment.Field()
    update_door = UpdateDoor.Field()
