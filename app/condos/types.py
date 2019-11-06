from graphene_django.types import DjangoObjectType
from .models import Block, Apartment

class BlockType(DjangoObjectType):
    class Meta:
        model = Block

class ApartmentType(DjangoObjectType):
    class Meta:
        model = Apartment
