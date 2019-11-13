"""
Queries that resolve residents ann list them
"""
import graphene
from graphql_jwt.decorators import superuser_required
from accounts.models import Resident
import accounts.utility as Utility
from accounts.types import ResidentType

class ResidentsQuery(graphene.AbstractType):
    """Used to read or fetch values"""
    residents = graphene.List(ResidentType)

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

    @superuser_required
    def resolve_residents(self, info, **kwargs):
        """Query all residents"""
        return Resident.objects.all()

    @superuser_required
    def resolve_resident(self, info, **kwargs):
        """Query a specific resident"""
        email = kwargs.get('email')
        cpf = kwargs.get('cpf')

        if email is not None:
            return Resident.objects.get(email=email)

        if cpf is not None:
            return Resident.objects.get(cpf=cpf)

        return None

    def resolve_voice_belongs_resident(self, info, **kwargs):
        """Find out if the voice belongs to the resident"""
        resident_cpf = kwargs.get('cpf')
        voice_data = kwargs.get('voice_data')
        mfcc_data = kwargs.get('mfcc_data')

        if voice_data is not None:
            voice_sample = Utility.json_voice_data_to_mfcc(voice_data)
        else:
            voice_sample = Utility.json_to_numpy_array(mfcc_data)

        resident = Resident.objects.get(cpf=resident_cpf)
        others_residents = Resident.objects.exclude(cpf=resident_cpf)

        companion_residents = ResidentsQuery._retrieve_random_residents(
                                                                    others_residents,
                                                                    quantity=4)
        test_group = [resident] + companion_residents

        query_result = False
        if resident == ResidentsQuery._find_nearest_resident_by_voice(test_group, voice_sample):
            query_result = True

        return query_result

    @staticmethod
    def _retrieve_random_residents(residents, quantity):
        """Pick up random residents"""
        residents = residents[::1]
        if len(residents) <= quantity:
            return residents

        secure_random = secrets.SystemRandom()
        random_residents = secure_random.sample(residents, quantity)

        return random_residents

    @staticmethod
    def _find_nearest_resident_by_voice(residents, voice_sample):
        """Find the nearest resident by the voice"""
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
