import graphene
from django.contrib.auth import get_user_model
from condos.models import Apartment, Block
from graphql_jwt.decorators import superuser_required, login_required
from accounts.models import Resident
from accounts.types import ResidentType, UserType, ResidentInput

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

        # TODO() - Remover um desses campos
        # talvez substituir voice_data por mfcc_data
        # A remoção é complicada pois existem dependencias
        voice_data = graphene.String()
        mfcc_data = graphene.String()

        mfcc_audio_speaking_name = graphene.String()
    def mutate(self, info, **kwargs):
        """Method to execute the mutation"""
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

        user.save()
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

class UpdateResident(graphene.Mutation):
    """Mutation from graphene for updating resident"""
    user = graphene.Field(UserType)
    resident = graphene.Field(ResidentType)

    class Arguments:
        """Mutation arguments for update a resident"""
        resident_data = ResidentInput()

    @login_required
    def mutate(self, info, resident_data=None):
        """Method to execute the mutation"""
        user = info.context.user
        if user.is_resident is False:
            raise Exception('User is not resident')
        email = user.email
        resident = Resident.objects.get(email=email)
        for key, value in resident_data.items():
            if (key == 'password') and (value is not None):
                user.set_password(resident_data.password)
            if (key == 'email') and (value is not None):
                setattr(user, key, value)
            if (key == 'email') and (value is not None):
                setattr(resident, key, value)
            else:
                setattr(resident, key, value)
        resident.save()
        user.save()
        return UpdateResident(user=user, resident=resident)

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
