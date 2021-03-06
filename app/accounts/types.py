"""Module for grouping Object Type setter functions"""
import graphene
from django.contrib.auth import get_user_model
from graphene_django import DjangoObjectType
from accounts.models import Visitor, Resident, Service, EntryVisitor, Entry, Admin

class ResidentType(DjangoObjectType):
    """Resident as a object type"""
    class Meta:
        """Metadata"""
        model = Resident

class EntryType(DjangoObjectType):
    """Entry as a object type"""
    class Meta:
        """Metadata"""
        model = Entry

class ServiceType(DjangoObjectType):
    """Service as a object type"""
    class Meta:
        """Metadata"""
        model = Service

class VisitorType(DjangoObjectType):
    """Visitor as a object type"""
    class Meta:
        """Metadata"""
        model = Visitor

class EntryVisitorType(DjangoObjectType):
    """EntryVisitor as a object type"""
    class Meta:
        """Metadata"""
        model = EntryVisitor

class UserType(DjangoObjectType):
    """User as a object type"""
    class Meta:
        """Metadata"""
        model = get_user_model()

class AdminType(DjangoObjectType):
    """Admin as a object type"""
    class Meta:
        """Metadata"""
        model = Admin

class ServiceInput(graphene.InputObjectType):
    """Service input data types"""
    password = graphene.String()
    email = graphene.String()
    complete_name = graphene.String()
    service_email = graphene.String(required=True)

class ResidentInput(graphene.InputObjectType):
    """Resident input data types"""
    complete_name = graphene.String()
    email = graphene.String()
    phone = graphene.String()
    resident_cpf = graphene.String(required=True)
    cpf = graphene.String()
    apartment = graphene.String()
    block = graphene.String()
    password = graphene.String()
    audio_speaking_phrase = graphene.List(graphene.Float)
    audio_speaking_name = graphene.List(graphene.Float)

class VisitorInput(graphene.InputObjectType):
    """Visitor input data types"""
    complete_name = graphene.String()
    cpf = graphene.String()
    visitor_cpf = graphene.String(required=True)
