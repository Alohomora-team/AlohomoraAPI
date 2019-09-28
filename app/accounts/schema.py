from django.contrib.auth import get_user_model

import graphene
from graphene_django import DjangoObjectType

from accounts.models import Visitor
from condos.models import Apartment, Block

from fastdtw import fastdtw
from python_speech_features import mfcc

import json
import random

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
        voice_data = graphene.String(required=True)

    def mutate(self, info, **kwargs):
        voice_data = _extract_mfcc_json(kwargs.get('voice_data'))
        cpf = kwargs.get('cpf')
        password = kwargs.get('password')
        complete_name = kwargs.get('complete_name')
        phone = kwargs.get('phone')
        email = kwargs.get('email')
        apartment = kwargs.get('apartment')
        block = kwargs.get('block')

        block_obj = Block.objects.get(number=block)


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

    def _extract_mfcc_json(voice_data):
        voice_data = json.loads(voice_data)
        voice_data = mfcc(voice_data, samplerate=16000)
        voice_data = json.dumps(voice_data)
        
        return voice_data

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
        voice_data = _extract_mfcc_json(kwargs.get('voice_data'))
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

    def _extract_mfcc_json(voice_data):
        voice_data = json.loads(voice_data)
        voice_data = mfcc(voice_data, samplerate=16000)
        voice_data = json.dumps(voice_data)
        
        return voice_data

class Mutation(graphene.ObjectType):
    create_user = CreateUser.Field()
    create_visitor = CreateVisitor.Field()

class Query(graphene.AbstractType):
    me = graphene.Field(UserType)
    users = graphene.List(UserType)
    visitors = graphene.List(VisitorType)
    voice_belongs_user = graphene.Boolean(
        cpf=graphene.String(required=True),
        voice_data=graphene.String(required=True)
    )

    def resolve_visitors(self, info, **kwargs):
        return Visitor.objects.all()

    def resolve_users(self, info, **kwargs):
        return get_user_model().objects.all()

    def resolve_me(self, info):
        user = info.context.user
        if user.is_anonymous:
            raise Exception('Not logged in!')

        return user

    def resolve_voice_belongs_user(self, info, **kwargs):
        user_cpf = kwargs.get('cpf')
        voice_data = json.loads(kwargs.get('voice_data'))
        voice_sample = mfcc(voice_data, samplerate=16000)

        user = get_user_model().objects.get(cpf=user_cpf)
        others = get_user_model().objects.exclude(cpf=user_cpf)
        companion_users = _retrieve_random_users(others, quantity=4)
        
        query_result = False
        test_group = [user] + companion_users
        if user == _find_nearest_user_by_voice(test_group, voice_sample):
            query_result = True

        return query_result

    def _retrieve_random_users(users, quantity):
        if len(users) <= quantity:
            return users

        random_users = list()
        users_len = len(users)

        while len(random_users) < quantity:
            current_random_user = users[random.randint(0,users_len - 1)]
            if random_users.count(current_random_user) == 0:
                random_users.append(current_random_user)

        return random_users

    def _find_nearest_user_by_voice(users, voice_sample):
        nearest_user = None
        lowest_dtw_score = 10**9

        for current_user in users:
            current_user_voice_data = json.loads(current_user.voice_data)
            current_measure = fastdtw(current_user_voice_data, voice_sample)
            if current_measure < lowest_dtw_score:
                lowest_dtw_score = current_measure
                nearest_user = current_user

        return nearest_user
        