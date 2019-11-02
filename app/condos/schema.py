import graphene
from .mutations.apartments import(
    CreateApartment,
    DeleteApartment,
    UpdateApartment,)
from .mutations.blocks import(
    CreateBlock,
    DeleteBlock,
    UpdateBlock,)

class Mutation(graphene.ObjectType):
    create_apartment = CreateApartment.Field()
    create_block = CreateBlock.Field()
    delete_block = DeleteBlock.Field()
    delete_apartment = DeleteApartment.Field()
    update_block = UpdateBlock.Field()
    update_apartment = UpdateApartment.Field()
