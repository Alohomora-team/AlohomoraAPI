from django.contrib.auth import get_user_model

import graphene
from graphene_django import DjangoObjectType

from accounts.models import Visitor, User
from condos.models import Apartment, Block

class UserType(DjangoObjectType):
    class Meta:
        model = User

class ServiceType(DjangoObjectType):
    class Meta:
        model = get_user_model()

class VisitorType(DjangoObjectType):
    class Meta:
        model = Visitor

class CreateService(graphene.Mutation):
    service = graphene.Field(ServiceType)


    class Arguments:
        username = graphene.String(required=True)
        password = graphene.String(required=True)
        email = graphene.String(required=True)

    def mutate(self, info, email, password, username):
        service = get_user_model()(
            username=username,
            email=email,
        )
        service.set_password(password)
        service.save()

        return CreateService(service=service)

class CreateUser(graphene.Mutation):
    user = graphene.Field(UserType)

    class Arguments:
        complete_name = graphene.String(required=True)
        email = graphene.String(required=True)
        phone = graphene.String(required=True)
        cpf = graphene.String(required=True)
        apartment = graphene.String(required=True)
        block = graphene.String(required=True)
        voice_data = graphene.String()

    def mutate(self, info, **kwargs):
        voice_data = kwargs.get('voice_data')
        cpf = kwargs.get('cpf')
        complete_name = kwargs.get('complete_name')
        phone = kwargs.get('phone')
        email = kwargs.get('email')
        apartment = kwargs.get('apartment')
        block = kwargs.get('block')

        block_obj = Block.objects.filter(number=block).first()

        if block_obj is None:
            raise Exception('Block not found')

        if Apartment.objects.filter(number=apartment, block=block_obj).first() is None:
            raise Exception('Apartment not found')


        user = User(
            complete_name=complete_name,
            email=email,
            phone=phone,
            cpf=cpf,
            voice_data=voice_data,
            apartment=Apartment.objects.get(number=apartment, block=block_obj))

        user.save()

        return CreateUser(user=user)

class CreateVisitor(graphene.Mutation):
    id = graphene.Int()
    complete_name = graphene.String()
    email = graphene.String()
    phone = graphene.String()
    cpf = graphene.String()
    voice_data = graphene.String()

    class Arguments:
        complete_name = graphene.String()
        email = graphene.String()
        phone = graphene.String()
        cpf = graphene.String()
        voice_data = graphene.String()
    def mutate(self, info, **kwargs):
        voice_data = kwargs.get('voice_data')
        cpf = kwargs.get('cpf')
        complete_name = kwargs.get('complete_name')
        phone = kwargs.get('phone')
        email = kwargs.get('email')

        visitor = Visitor(
            complete_name=complete_name,
            email=email,
            phone=phone,
            cpf=cpf,
            voice_data=voice_data,
        )
        visitor.save()

        return CreateVisitor(
            id=visitor.id,
            complete_name=visitor.complete_name,
            email=visitor.email,
            phone=visitor.phone,
            cpf=visitor.cpf,
            voice_data=visitor.voice_data,
        )

class Mutation(graphene.ObjectType):
    create_user = CreateUser.Field()
    create_visitor = CreateVisitor.Field()
    create_service = CreateService.Field()

class Query(graphene.AbstractType):
    me = graphene.Field(ServiceType)
    users = graphene.List(UserType)
    visitors = graphene.List(VisitorType)
    services = graphene.List(ServiceType)


    def resolve_visitors(self, info, **kwargs):
        return Visitor.objects.all()

    def resolve_users(self, info, **kwargs):
        return User.objects.all()

    def resolve_me(self, info):
        service = info.context.user
        if service.is_anonymous:
            raise Exception('Not logged in!')

        return service
