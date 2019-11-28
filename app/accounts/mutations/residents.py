"""
Creates a CRUD to Resident model
"""
import numpy
import graphene
from python_speech_features import mfcc
from django.contrib.auth import get_user_model
from condos.models import Apartment, Block
from graphql_jwt.decorators import superuser_required, login_required
from accounts.models import Resident
from accounts.types import ResidentType, UserType, ResidentInput
import accounts.utility as Utility


class CreateResident(graphene.Mutation):
    """Mutation from graphene for creating resident"""

    resident = graphene.Field(ResidentType)

    class Arguments:
        """Mutation arguments for create a resident"""
        complete_name = graphene.String(required=True)
        email = graphene.String(required=True)
        phone = graphene.String(required=True)
        cpf = graphene.String(required=True)
        apartment = graphene.String(required=True)
        block = graphene.String(required=True)
        password = graphene.String(required=False)

        audio_speaking_phrase = graphene.List(graphene.Float, required=True)
        audio_speaking_name = graphene.List(graphene.Float, required=True)
        audio_samplerate = graphene.Int(required=False)

    @staticmethod
    def _set_sample_rate(audio_samplerate):
        """
        Set sample_rate to default (1600 hz)
        """

        if audio_samplerate is None:
            audio_samplerate = 1600

        return audio_samplerate

    @staticmethod
    def _verify_block(block):
        """
        Raise a exception if block not exists
        """
        if block is None:
            raise Exception('Block not found')

    @staticmethod
    def _if_aparment_exists(apartment, block):
        """
        Raise a exception if block not exists
        """

        query = Apartment.objects.filter(
            number=apartment,
            block=block
        ).first()

        if query is None:
            raise Exception('Apartment not found')

    @superuser_required
    def mutate(self, info, **kwargs):
        """Method to execute the mutation"""

        cpf = kwargs.get('cpf')
        complete_name = kwargs.get('complete_name')
        phone = kwargs.get('phone')
        email = kwargs.get('email')
        apartment = kwargs.get('apartment')
        block = kwargs.get('block')
        password = kwargs.get('password')

        audio_speaking_phrase = kwargs.get('audio_speaking_phrase')
        audio_speaking_name = kwargs.get('audio_speaking_name')
        audio_samplerate = kwargs.get('audio_samplerate')

        user = get_user_model()(email=email)
        user.set_password(password)
        user.is_resident = True

        block_obj = Block.objects.filter(number=block).first()

        CreateResident._verify_block(block_obj)
        CreateResident._if_aparment_exists(apartment, block_obj)
        audio_samplerate = CreateResident._set_sample_rate(audio_samplerate)

        audio_speaking_phrase = Utility.treat_audio_data(audio_speaking_phrase, audio_samplerate)
        mfcc_audio_speaking_phrase = Utility.create_model_mfcc(
            audio_speaking_phrase,
            audio_samplerate
        )

        audio_speaking_name = Utility.treat_audio_data(audio_speaking_name, audio_samplerate)
        mfcc_audio_speaking_name = Utility.create_model_mfcc(
            audio_speaking_name,
            audio_samplerate
        )

        user.save()
        resident = Resident.objects.create(user=user)
        resident = Resident(
            complete_name=complete_name,
            email=email,
            phone=phone,
            cpf=cpf,
            user=user,
            apartment=Apartment.objects.get(number=apartment, block=block_obj),
            mfcc_audio_speaking_phrase=mfcc_audio_speaking_phrase,
            mfcc_audio_speaking_name=mfcc_audio_speaking_name
        )
        resident.save()
        return CreateResident(resident=resident)

class UpdateResident(graphene.Mutation):
    """Mutation from graphene for updating resident"""
    resident = graphene.Field(ResidentType)

    class Arguments:
        """Mutation arguments for update a resident"""
        resident_data = ResidentInput()

    @login_required
    def mutate(self, info, resident_data=None):
        """Method to execute the mutation"""
        resident = Resident.objects.get(cpf=resident_data.resident_cpf)
        for key, value in resident_data.items():
            setattr(resident, key, value)
        resident.save()
        return UpdateResident(resident=resident)

class DeleteResident(graphene.Mutation):
    """Mutation from graphene for deleting resident"""
    resident_email = graphene.String()

    class Arguments:
        """Mutation arguments for delete a resident"""
        resident_email = graphene.String(required=True)

    @superuser_required
    def mutate(self, info, resident_email):
        """Method to execute the mutation"""
        resident = Resident.objects.get(email=resident_email)
        user = get_user_model().objects.get(email=resident_email)
        user.delete()
        resident.delete()
