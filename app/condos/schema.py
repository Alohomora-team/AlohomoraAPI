import graphene

from graphene_django.types import DjangoObjectType

from condos.models import Block, Apartment

class BlockType(DjangoObjectType):
    class Meta:
        model = Block
  
class ApartmentType(DjangoObjectType):
    class Meta:
        model = Apartment
  
class Query(object):
    all_blocks = graphene.List(BlockType)
    all_apartments = graphene.List(ApartmentType)

    def resolve_all_blocks(self, info, **kwargs):
        return Block.objects.all()

    def resolve_all_apartments(self, info, **kwargs):
        return Apartment.objects.select_related('block').all()



