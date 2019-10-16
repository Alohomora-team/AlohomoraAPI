import secrets
import graphene
from graphene_django import DjangoObjectType
from accounts.models import Visitor, Resident, Service
import accounts.utility as Utility
from condos.models import Apartment, Block
from django.contrib.auth import get_user_model
from graphql_jwt.decorators import superuser_required, login_required

class ResidentType(DjangoObjectType):
    class Meta:
        model = Resident

class ServiceType(DjangoObjectType):
    class Meta:
        model = Service

class VisitorType(DjangoObjectType):
    class Meta:
        model = Visitor

class UserType(DjangoObjectType):
    class Meta:
        model = get_user_model()

class CreateUser(graphene.Mutation):
    """Mutation from graphene for creating service"""
    user = graphene.Field(UserType)
    class Arguments:
        username = graphene.String(required=True)
        password = graphene.String(required=False)

    def mutate(self, info, password, username):
        user = get_user_model()(
            username=username,
            password=password,
        )
        user.set_password(password)
        user.save()

        return CreateUser(user=user)

class CreateService(graphene.Mutation):
    """Mutation from graphene for creating service"""

    service = graphene.Field(ServiceType)

    class Arguments:
        password = graphene.String(required=True)
        email = graphene.String(required=True)
        complete_name = graphene.String(required=True)

    def mutate(self, info, email, password, complete_name):
        user = get_user_model()(email=email)
        user.set_password(password)
        user.is_service = True
        user.save()
        service = Service.objects.create(user=user)

        service = Service(
            complete_name=complete_name,
            email=email,
            user=user,
        )
        service.save()

        return CreateService(service=service)

class CreateResident(graphene.Mutation):
    """Mutation from graphene for creating user"""

    resident = graphene.Field(ResidentType)

    class Arguments:
        complete_name = graphene.String(required=True)
        email = graphene.String(required=True)
        phone = graphene.String(required=True)
        cpf = graphene.String(required=True)
        apartment = graphene.String(required=True)
        block = graphene.String(required=True)
        password = graphene.String(required=False)

        # TODO() - Remover um desses campos
        # talvez substituir voice_data por mfcc_data
        # A remoção é complicada pois existem dependencias
        voice_data = graphene.String()
        mfcc_data = graphene.String()

        mfcc_audio_speaking_name = graphene.String()

    def mutate(self, info, **kwargs):
        voice_data = kwargs.get('voice_data')
        mfcc_data = kwargs.get('mfcc_data')
        cpf = kwargs.get('cpf')
        complete_name = kwargs.get('complete_name')
        phone = kwargs.get('phone')
        email = kwargs.get('email')
        apartment = kwargs.get('apartment')
        block = kwargs.get('block')
        password = kwargs.get('password')
        mfcc_audio_speaking_name = kwargs.get('mfcc_audio_speaking_name')

        user = get_user_model()(email=email)
        user.set_password(password)
        user.is_resident = True
        user.save()

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

        resident = Resident.objects.create(user=user)

        resident = Resident(
            complete_name=complete_name,
            email=email,
            phone=phone,
            cpf=cpf,
            voice_data=voice_data,
            user=user,
            apartment=Apartment.objects.get(number=apartment, block=block_obj),
            mfcc_audio_speaking_name=mfcc_audio_speaking_name
        )

        resident.save()

        return CreateResident(resident=resident)

class CreateVisitor(graphene.Mutation):
    """Mutation from graphene for creating visitor"""
    visitor = graphene.Field(VisitorType)

    class Arguments:
        complete_name = graphene.String()
        email = graphene.String()
        phone = graphene.String()
        cpf = graphene.String()
        voice_data = graphene.String()
        owner_cpf = graphene.String()

    @login_required
    def mutate(self, info, **kwargs):
        voice_data = kwargs.get('voice_data')
        cpf = kwargs.get('cpf')
        complete_name = kwargs.get('complete_name')
        phone = kwargs.get('phone')
        email = kwargs.get('email')
        owner_cpf = kwargs.get('owner_cpf')

        resident = Resident.objects.filter(cpf=owner_cpf).first()

        if voice_data is not None:
            voice_data = Utility.json_voice_data_to_json_mfcc(voice_data)

        visitor = Visitor(
            complete_name=complete_name,
            email=email,
            cpf=cpf,
            phone=phone,
            voice_data=voice_data,
            owner=resident,
        )
        visitor.save()

        return CreateVisitor(visitor=visitor)

class ActivateUser(graphene.Mutation):
    """Mutation from graphene for activating user"""
    user = graphene.Field(UserType)

    class Arguments:
        user_email = graphene.String()
    def mutate(self, info, user_email):
        user = get_user_model().objects.get(email=user_email)
        user.is_active = True
        user.save()
        return ActivateUser(user=user)

class DeactivateUser(graphene.Mutation):
    """Mutation from graphene for activating user"""
    user = graphene.Field(UserType)

    class Arguments:
        user_email = graphene.String()
    def mutate(self, info, user_email):
        user = get_user_model().objects.get(email=user_email)
        user.is_active = False
        user.save()
        return ActivateUser(user=user)

class Mutation(graphene.ObjectType):
    """Used to write or post values"""

    create_user = CreateUser.Field()
    create_visitor = CreateVisitor.Field()
    create_service = CreateService.Field()
    create_resident = CreateResident.Field()
    activate_user = ActivateUser.Field()
    deactivate_user = DeactivateUser.Field()

class Query(graphene.AbstractType):
    """Used to read or fetch values"""

    me = graphene.Field(UserType)
    residents = graphene.List(ResidentType)
    visitors = graphene.List(VisitorType)
    services = graphene.List(ServiceType)
    users = graphene.List(UserType)

    voice_belongs_resident = graphene.Boolean(
        cpf=graphene.String(required=True),
        # TODO() - Remover um desses campos
        # talvez substituir voice_data por mfcc_data
        # A remoção é complicada pois existem dependencias
        voice_data=graphene.String(),
        mfcc_data=graphene.String()
    )

    resident = graphene.Field(
        ResidentType,
        email=graphene.String(),
        cpf=graphene.String()
        )

    visitor = graphene.Field(
        VisitorType,
        email=graphene.String(),
        cpf=graphene.String()
        )
    @superuser_required
    def resolve_visitors(self, info, **kwargs):
        return Visitor.objects.all()
    @superuser_required
    def resolve_residents(self, info, **kwargs):
        return Resident.objects.all()
    @superuser_required
    def resolve_services(self, info, **kwargs):
        return Service.objects.all()
    @superuser_required
    def resolve_users(self, info, **kwargs):
        return get_user_model().objects.all()
    @superuser_required
    def resolve_resident(self, info, **kwargs):
        email = kwargs.get('email')
        cpf = kwargs.get('cpf')

        if email is not None:
            return Resident.objects.get(email=email)

        if cpf is not None:
            return Resident.objects.get(cpf=cpf)

        return None
    @superuser_required
    def resolve_visitor(self, info, **kwargs):
        email = kwargs.get('email')
        cpf = kwargs.get('cpf')

        if email is not None:
            return Visitor.objects.get(email=email)

        if cpf is not None:
            return Visitor.objects.get(cpf=cpf)

        return None
    def resolve_me(self, info):
        user = info.context.user
        if user.is_active is not True:
            raise Exception('User is NOT active')
        if user.is_service is True:
            raise Exception('User is service')
        if user.is_visitor is True:
            raise Exception('User is visitor')
        if user.is_resident is True:
            raise Exception('User is resident')
        return user

    def resolve_voice_belongs_resident(self, info, **kwargs):
        resident_cpf = kwargs.get('cpf')
        voice_data = kwargs.get('voice_data')
        mfcc_data = kwargs.get('mfcc_data')

        if voice_data is not None:
            voice_sample = Utility.json_voice_data_to_mfcc(voice_data)
        else:
            voice_sample = Utility.json_to_numpy_array(mfcc_data)

        resident = Resident.objects.get(cpf=resident_cpf)
        others_residents = Resident.objects.exclude(cpf=resident_cpf)

        companion_residents = Query._retrieve_random_residents(others_residents, quantity=4)
        test_group = [resident] + companion_residents

        query_result = False
        if resident == Query._find_nearest_resident_by_voice(test_group, voice_sample):
            query_result = True

        return query_result

    @staticmethod
    def _retrieve_random_residents(residents, quantity):
        residents = residents[::1]
        if len(residents) <= quantity:
            return residents

        secure_random = secrets.SystemRandom()
        random_residents = secure_random.sample(residents, quantity)

        return random_residents

    @staticmethod
    def _find_nearest_resident_by_voice(residents, voice_sample):
        nearest_resident = None
        lowest_dtw_score = 10**9

        for current_resident in residents:
            current_resident_voice_data = Utility.json_to_numpy_array(current_resident.voice_data)
            current_measure = Utility.compute_dtw_distance(voice_sample,
                                                           current_resident_voice_data)

            if current_measure < lowest_dtw_score:
                lowest_dtw_score = current_measure
                nearest_resident = current_resident

        return nearest_resident
