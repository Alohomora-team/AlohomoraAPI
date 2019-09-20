from django.contrib.auth import get_user_model

import graphene
from graphene_django import DjangoObjectType

from accounts.models import Visitor

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
        cpf = graphene.Int(required=True)
        voice_data = graphene.String()


    def mutate(self, info, complete_name, password, email, phone, cpf, voice_data):
        user = get_user_model()(
            complete_name=complete_name,
            email=email,
            phone=phone,
            cpf=cpf,
            voice_data=voice_data,
        )
        user.set_password(password)
        user.save()

        return CreateUser(user=user)

class CreateVisitor(graphene.Mutation):
    id = graphene.Int()
    complete_name = graphene.String()
    email = graphene.String()
    phone = graphene.String()
    cpf = graphene.Int()
    voice_data = graphene.String()
    user = graphene.Field(UserType)

    class Arguments:
        complete_name = graphene.String()
        email = graphene.String()
        phone = graphene.String()
        cpf = graphene.Int()
        voice_data = graphene.String()
        user_id = graphene.Int()

    def mutate(self, info, complete_name, email, phone, cpf, voice_data, user_id):
        user = get_user_model().objects.filter(id=user_id).first()
        if not user:
            raise Exception('Invalid User!')
        if user.is_authenticated:
            raise Exception('Not logged in!')

        visitor = Visitor(
            complete_name=complete_name,
            email=email,
            phone=phone,
            cpf=cpf,
            voice_data=voice_data,
        )
        Visitor.objects.create(
            user=user,
        )
        visitor.save()

        return CreateVisitor(
            id=visitor.id,
            complete_name=visitor.complete_name,
            email=visitor.email,
            phone=visitor.phone,
            cpf=visitor.cpf,
            voice_data=visitor.voice_data,
            user=user,
        )

class Mutation(graphene.ObjectType):
    create_user = CreateUser.Field()
    create_visitor = CreateVisitor.Field()

class Query(graphene.AbstractType):
    me = graphene.Field(UserType)
    users = graphene.List(UserType)
    visitors = graphene.List(VisitorType)

    def resolve_me(self, info):
        user = info.context.user
        if user.is_anonymous:
            raise Exception('Not logged in!')

    def resolve_visitors(self, info, **kwargs):
        return Visitor.objects.all()

    def resolve_users(self, info, **kwargs):
        return get_user_model().objects.all()


        return user
