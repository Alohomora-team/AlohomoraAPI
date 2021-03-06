"""
Queries that resolve residents ann list them
"""
import secrets
import numpy
from python_speech_features import mfcc
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
        audio_speaking_phrase=graphene.List(graphene.Float, required=True),
        audio_samplerate=graphene.Int(required=False)
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
        audio_speaking_phrase = kwargs.get('audio_speaking_phrase')
        audio_samplerate = kwargs.get('audio_samplerate')

        if audio_samplerate is None:
            audio_samplerate = 16000

        audio_speaking_phrase = Utility.treat_audio_data(audio_speaking_phrase, audio_samplerate)

        mfcc_audio_speaking_phrase = mfcc(
            audio_speaking_phrase,
            samplerate=16000,
            winfunc=numpy.hamming
        )

        main_resident, resident_test_group = ResidentsQuery._create_test_group(
            resident_cpf,
            group_size=10
        )

        print("\n------")
        print(f"Comparing {main_resident.complete_name} against others residents ...\n\n")
        nearest_resident = ResidentsQuery._find_nearest_resident_by_mfcc_phrase(
            residents=resident_test_group,
            mfcc_attribute=mfcc_audio_speaking_phrase
        )

        if main_resident != nearest_resident:
            print(f"Expected resident: {main_resident.complete_name}")
            print(f"Nearest: {nearest_resident.complete_name}")
            return False
        else:
            print("Resident voice matches!")
            return True

    @staticmethod
    def _create_test_group(main_resident_cpf, group_size):
        """
        Set up a resident group including the main resident
        used to make comparisons against given audios data
        """

        main_resident = Resident.objects.get(cpf=main_resident_cpf)

        resident_group = Resident.objects.exclude(cpf=main_resident_cpf)[::1]
        group_size = min(len(resident_group), group_size - 1)
        resident_group = secrets.SystemRandom().sample(resident_group, group_size)

        return main_resident, resident_group+[main_resident]

    @staticmethod
    def _find_nearest_resident_by_mfcc_phrase(residents, mfcc_attribute):
        """
        Find out the nearest resident based on mfcc_audio_speaking_phrase
        """
        nearest_resident = None
        lowest_dtw_score = (1 << 64) - 1
        error_const = 0.94

        for resident in residents:
            resident_mfcc_attribute = resident.mfcc_audio_speaking_phrase
            resident_mfcc_attribute = Utility.mfcc_array_to_matrix(resident_mfcc_attribute)
            resident_mfcc_attribute = numpy.array(resident_mfcc_attribute)

            current_measure = Utility.compute_dtw_distance(mfcc_attribute, resident_mfcc_attribute)
            print(f"\tDifferences to {resident.complete_name} is {current_measure}")
            if current_measure * error_const < lowest_dtw_score:
                lowest_dtw_score = current_measure
                nearest_resident = resident

        return nearest_resident
