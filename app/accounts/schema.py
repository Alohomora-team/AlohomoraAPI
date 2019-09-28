from django.contrib.auth import get_user_model

import graphene
from graphene_django import DjangoObjectType

from accounts.models import Visitor
from condos.models import Apartment, Block

class UserType(DjangoObjectType):
    class Meta:
        model = get_user_model()

class VisitorType(DjangoObjectType):
    class Meta:
        model = Visitor

class CreateUser(graphene.Mutation):
    user = graphene.Field(UserType)

    class Arguments:
        complete_name = graphene.String(required=True)
        password = graphene.String(required=True)
        email = graphene.String(required=True)
        phone = graphene.String(required=True)
        cpf = graphene.String(required=True)
        apartment = graphene.String(required=True)
        block = graphene.String(required=True)
        voice_data = graphene.String()

    def mutate(self, info, **kwargs):
        voice_data = kwargs.get('voice_data')
        cpf = kwargs.get('cpf')
        password = kwargs.get('password')
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


        user = get_user_model()(
            complete_name=complete_name,
            email=email,
            phone=phone,
            cpf=cpf,
            voice_data=voice_data,
            username=email,
            apartment=Apartment.objects.get(number=apartment, block=block_obj))

        user.set_password(password)
        user.save()

        return CreateUser(user=user)

class CreateVisitor(graphene.Mutation):
    id = graphene.Int()
    complete_name = graphene.String()
    email = graphene.String()
    phone = graphene.String()
    cpf = graphene.String()
    voice_data = graphene.String()
    owner = graphene.Field(UserType)

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

        user = info.context.user or None
        if not user:
            raise Exception('Invalid User!')
        if not user.is_authenticated:
            raise Exception('Not logged in!')

        visitor = Visitor(
            complete_name=complete_name,
            email=email,
            phone=phone,
            cpf=cpf,
            voice_data=voice_data,
            owner=user,
        )
        visitor.save()

        return CreateVisitor(
            id=visitor.id,
            complete_name=visitor.complete_name,
            email=visitor.email,
            phone=visitor.phone,
            cpf=visitor.cpf,
            voice_data=visitor.voice_data,
            owner=user.owner,
        )

class Mutation(graphene.ObjectType):
    create_user = CreateUser.Field()
    create_visitor = CreateVisitor.Field()

class Query(graphene.AbstractType):
    me = graphene.Field(UserType)
    users = graphene.List(UserType)
    visitors = graphene.List(VisitorType)

    user = graphene.Field(
        UserType,
        email=graphene.String(),
        cpf=graphene.String()
        )

    visitor = graphene.Field(
        VisitorType,
        email=graphene.String(),
        cpf=graphene.String()
        )


    def resolve_visitors(self, info, **kwargs):
        return Visitor.objects.all()

    def resolve_users(self, info, **kwargs):
        return get_user_model().objects.all()

    def resolve_user(self, info, **kwargs):
        email = kwargs.get('email')
        cpf = kwargs.get('cpf')

        if email is not None:
            return get_user_model().objects.filter(email=email).first()

        if cpf is not None:
            return get_user_model().objects.filter(cpf=cpf).first()

        return None

    def resolve_visitor(self, info, **kwargs):
        email = kwargs.get('email')
        cpf = kwargs.get('cpf')

        if email is not None:
            return Visitor.objects.filter(email=email).first()

        if cpf is not None:
            return Visitor.objects.filter(cpf=cpf).first()

        return None

    def resolve_me(self, info):
        user = info.context.user
        if user.is_anonymous:
            raise Exception('Not logged in!')

        return user
