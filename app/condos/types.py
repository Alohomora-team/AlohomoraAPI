"""
Binds of django models to graphql types
"""

from graphene_django.types import DjangoObjectType
from .models import Block, Apartment

class BlockType(DjangoObjectType):
    """
    Bind Block model to BlockType graphql type
    """
    class Meta:
        """Meta class"""
        model = Block

class ApartmentType(DjangoObjectType):
    """
    Bind Apartment model to Apartment graphql type
    """
    class Meta:
        """Meta class"""
        model = Apartment
