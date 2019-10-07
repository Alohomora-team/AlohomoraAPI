import secrets
import graphene
from graphene_django import DjangoObjectType
from accounts.models import Visitor, User
import accounts.utility as Utility
from condos.models import Apartment, Block
from django.contrib.auth import get_user_model

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
    """Mutation from graphene for creating service"""

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
    """Mutation from graphene for creating user"""

    user = graphene.Field(UserType)

    class Arguments:
        complete_name = graphene.String(required=True)
        email = graphene.String(required=True)
        phone = graphene.String(required=True)
        cpf = graphene.String(required=True)
        apartment = graphene.String(required=True)
        block = graphene.String(required=True)
        voice_data = graphene.String()
        mfcc_data = graphene.String()

    def mutate(self, info, **kwargs):
        voice_data = kwargs.get('voice_data')
        mfcc_data = kwargs.get('mfcc_data')
        cpf = kwargs.get('cpf')
        complete_name = kwargs.get('complete_name')
        phone = kwargs.get('phone')
        email = kwargs.get('email')
        apartment = kwargs.get('apartment')
        block = kwargs.get('block')

        block_obj = Block.objects.filter(number=block).first()

        if voice_data is not None:
            try:
                voice_data = Utility.json_voice_data_to_json_mfcc(voice_data)
            except:
                raise Exception('Invalid voice data')
        else:
            voice_data = mfcc_data

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
    """Mutation from graphene for creating visitor"""

    id = graphene.Int()
    complete_name = graphene.String()
    email = graphene.String()
    phone = graphene.String()
    cpf = graphene.String()
    voice_data = graphene.String()
    owner = graphene.Field(UserType)
    owner_cpf = graphene.String()

    class Arguments:
        complete_name = graphene.String()
        email = graphene.String()
        phone = graphene.String()
        cpf = graphene.String()
        voice_data = graphene.String()
        owner_cpf = graphene.String()

    def mutate(self, info, **kwargs):
        voice_data = kwargs.get('voice_data')
        cpf = kwargs.get('cpf')
        complete_name = kwargs.get('complete_name')
        phone = kwargs.get('phone')
        email = kwargs.get('email')
        owner_cpf = kwargs.get('owner_cpf')

        user = User.objects.filter(cpf=owner_cpf).first()

        if voice_data is not None:
            voice_data = Utility.json_voice_data_to_json_mfcc(voice_data)

        visitor = Visitor(
            complete_name=complete_name,
            email=email,
            cpf=cpf,
            phone=phone,
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
            owner=visitor.owner,
        )

class Mutation(graphene.ObjectType):
    """Used to write or post values"""

    create_user = CreateUser.Field()
    create_visitor = CreateVisitor.Field()
    create_service = CreateService.Field()

class Query(graphene.AbstractType):
    """Used to read or fetch values"""

    me = graphene.Field(ServiceType)
    users = graphene.List(UserType)
    visitors = graphene.List(VisitorType)
    services = graphene.List(ServiceType)

    voice_belongs_user = graphene.Boolean(
        cpf=graphene.String(required=True),
        voice_data=graphene.String(),
        mfcc_data=graphene.String()
    )

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
        return User.objects.all()

    def resolve_services(self, info, **kwargs):
        return get_user_model().objects.all()

    def resolve_user(self, info, **kwargs):
        email = kwargs.get('email')
        cpf = kwargs.get('cpf')

        if email is not None:
            return User.objects.get(email=email)

        if cpf is not None:
            return User.objects.get(cpf=cpf)

        return None

    def resolve_visitor(self, info, **kwargs):
        email = kwargs.get('email')
        cpf = kwargs.get('cpf')

        if email is not None:
            return Visitor.objects.get(email=email)

        if cpf is not None:
            return Visitor.objects.get(cpf=cpf)

        return None

    def resolve_me(self, info):
        service = info.context.user
        if service.is_anonymous:
            raise Exception('Not logged in!')

        return service

    def resolve_voice_belongs_user(self, info, **kwargs):
        user_cpf = kwargs.get('cpf')
        voice_data = kwargs.get('voice_data')
        mfcc_data = kwargs.get('mfcc_data')

        if voice_data is not None:
            voice_sample = Utility.json_voice_data_to_mfcc(voice_data)
        else:
            voice_sample = Utility.json_to_numpy_array(mfcc_data)

        user = User.objects.get(cpf=user_cpf)
        others_users = User.objects.exclude(cpf=user_cpf)

        companion_users = Query._retrieve_random_users(others_users, quantity=4)
        test_group = [user] + companion_users

        query_result = False
        if user == Query._find_nearest_user_by_voice(test_group, voice_sample):
            query_result = True

        return query_result

    @staticmethod
    def _retrieve_random_users(users, quantity):
        users = users[::1]
        if len(users) <= quantity:
            return users

        secure_random = secrets.SystemRandom()
        random_users = secure_random.sample(users, quantity)

        return random_users

    @staticmethod
    def _find_nearest_user_by_voice(users, voice_sample):
        nearest_user = None
        lowest_dtw_score = 10**9

        for current_user in users:
            current_user_voice_data = Utility.json_to_numpy_array(current_user.voice_data)
            current_measure = Utility.compute_dtw_distance(voice_sample, current_user_voice_data)

            if current_measure < lowest_dtw_score:
                lowest_dtw_score = current_measure
                nearest_user = current_user

        return nearest_user
