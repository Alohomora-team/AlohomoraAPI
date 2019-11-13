"""
Queries that resolve residents ann list them
"""
import graphene
from graphql_jwt.decorators import superuser_required
from accounts.models import Resident
import accounts.utility as Utility
from accounts.types import ResidentType
from python_speech_features import mfcc
import numpy

class ResidentsQuery(graphene.AbstractType):
    """Used to read or fetch values"""
    residents = graphene.List(ResidentType)

    voice_belongs_resident = graphene.Boolean(
        cpf=graphene.String(required=True),
        audio_speaking_phrase=graphene.List(graphene.Float, required=True)
        audio_speaking_name=graphene.List(graphene.Float, required=False)
        audio_samplerate=graphene.Int(required=False)
    )

    resident = graphene.Field(
        ResidentType,
        email=graphene.String(),
        cpf=graphene.String()
        )

    # @superuser_required
    def resolve_residents(self, info, **kwargs):
        """Query all residents"""
        return Resident.objects.all()

    # @superuser_required
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
        audio_speaking_name = kwargs.get('audio_speaking_name')
        audio_samplerate = kwargs.get('audio_samplerate')

        if audio_samplerate is None:
            audio_samplerate = 16000

        mfcc_audio_speaking_phrase = mfcc(
            numpy.array(audio_speaking_phrase),
            samplerate=audio_samplerate,
            winfunc=numpy.hamming
        )

        resident = Resident.objects.get(cpf=resident_cpf)
        others_residents = Resident.objects.exclude(cpf=resident_cpf)

        companion_residents = ResidentsQuery._retrieve_random_residents(
            others_residents,
            quantity=4
        )

        test_group = [resident] + companion_residents

        audio_phrase_belongs_resident = False
        if resident == ResidentsQuery._find_nearest_resident_by_voice(test_group, mfcc_audio_speaking_phrase):
            audio_phrase_belongs_resident = True

        audio_name_belongs_resident = True
        if audio_speaking_name is not None:
            mfcc_audio_speaking_name = mfcc(
                numpy.array(audio_speaking_name),
                samplerate=audio_samplerate,
                winfunc=numpy.hamming
            )

            if resident == ResidentsQuery._find_nearest_resident_by_name(test_group, mfcc_audio_speaking_name):
                audio_name_belongs_resident = True

        return audio_phrase_belongs_resident and audio_name_belongs_resident

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
        lowest_dtw_score = (1 << 64) - 1

        for resident in residents:
            resident_voice_data = Utility.mfcc_array_to_matrix(resident.mfcc_audio_speaking_phrase)
            resident_voice_data = numpy.array(resident_voice_data)

            current_mease = Utility.compute_dtw_distance(voice_sample, resident_voice_data)
            if current_measure < lowest_dtw_score:
                lowest_dtw_score = current_measure
                nearest_resident = current_resident

        return nearest_resident

    @staticmethod
    def _find_nearest_resident_by_name(residents, audio_sample):
        nearest_resident = None
        lowest_dtw_score = (1 << 64) - 1

        for resident in residents:
            resident_audio_sample = Utility.mfcc_array_to_matrix(resident.mfcc_audio_speaking_name)
            resident_audio_sample = numpy.array(resident_audio_sample)

            current_measure = Utility.compute_dtw_distance(audio_sample, resident_audio_sample)
            if current_measure < lowest_dtw_score:
                lowest_dtw_score = current_measure
                nearest_resident = resident

        return nearest_resident
