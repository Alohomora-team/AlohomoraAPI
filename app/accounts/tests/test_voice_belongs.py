import json
from django.contrib.auth import get_user_model
from django.test import TestCase
from graphene.test import Client
from alohomora.schema import schema
import accounts.utility as Utility
from accounts.models import Resident
from graphql_jwt.testcases import JSONWebTokenTestCase
from python_speech_features import mfcc
import numpy
import accounts.utility as Utility

class VoiceBelongsUserTests(TestCase):
    """Test using mfcc and fastwd for voice recognition and authentication"""
    def setUp(self):
        self.client = Client(schema)
        self.query = '''
            query voiceBelongsResident(
                $cpf: String!,
                $audioSpeakingPhrase: [Float]!,
                $audioSpeakingName: [Float],
                $audioSamplerate: Int
            ){
                voiceBelongsResident(
                    cpf: $cpf,
                    audioSpeakingPhrase: $audioSpeakingPhrase,
                    audioSpeakingName: $audioSpeakingName,
                    audioSamplerate: $audioSamplerate
                )
            }
        '''

    @classmethod
    def setUpTestData(cls):
        mfcc_1 = Utility.create_model_mfcc(
            [x for x in range(32073)],
            samplerate=16000
        )
        mfcc_2 = Utility.create_model_mfcc(
            [3 * x for x in range(32073)],
            samplerate=16000
        )
        mfcc_3 = Utility.create_model_mfcc(
            [x**2  - 50 * x + 20 for x in range(32073)],
            samplerate=16000
        )
        mfcc_4 = Utility.create_model_mfcc(
            [x - 200 for x in range(32073)],
            samplerate=16000
        )
        mfcc_5 = Utility.create_model_mfcc(
            [x * 0.5 for x in range(32073)],
            samplerate=16000
        )

        get_user_model().objects.create(
            email='resident1@example.com',
            password='resident1-password',
        )
        get_user_model().objects.create(
            email='resident2@example.com',
            password='resident2-password',
        )
        get_user_model().objects.create(
            email='resident3@example.com',
            password='resident3-password',
        )
        get_user_model().objects.create(
            email='resident4@example.com',
            password='resident4-password',
        )
        get_user_model().objects.create(
            email='resident5@example.com',
            password='resident5-password',
        )

        Resident.objects.create(
            complete_name="Barry Allen",
            email="love_you_iris@starslab.com",
            phone="6133941598",
            user=get_user_model().objects.get(email='resident1@example.com'),
            cpf="0123456789",
            mfcc_audio_speaking_phrase=mfcc_1,
            mfcc_audio_speaking_name=mfcc_1,
        )

        Resident.objects.create(
            complete_name="Naruto Uzumaku",
            email="sereihokage@konoha.com",
            phone="6133941597",
            cpf="0123456781",
            user=get_user_model().objects.get(email='resident2@example.com'),
            mfcc_audio_speaking_phrase=mfcc_2,
            mfcc_audio_speaking_name=mfcc_2,
        )

        Resident.objects.create(
            complete_name="Max Steel",
            email="modoturbo@yahoo.com",
            phone="6133941596",
            cpf="0123456782",
            user=get_user_model().objects.get(email='resident3@example.com'),
            mfcc_audio_speaking_phrase=mfcc_3,
            mfcc_audio_speaking_name=mfcc_3,
        )

        Resident.objects.create(
            complete_name="Benjamin Tennyson",
            email="ben10@omnitrix.com",
            phone="33941595",
            cpf="0123456783",
            user=get_user_model().objects.get(email='resident4@example.com'),
            mfcc_audio_speaking_phrase=mfcc_4,
            mfcc_audio_speaking_name=mfcc_4,
        )

        Resident.objects.create(
            complete_name="Eren Jaeger",
            email="i_hate_marleyans@eldia.com",
            phone="99999999",
            cpf="0000000000",
            user=get_user_model().objects.get(email='resident5@example.com'),
            mfcc_audio_speaking_phrase=mfcc_5,
            mfcc_audio_speaking_name=mfcc_5,
        )

    def test_query_accuracy_true(self):
        response = self.client.execute(
            self.query,
            variables={
                'cpf': '0123456789',
                'audioSpeakingPhrase': [x for x in range(32073)],
                'audioSpeakingName': [x for x in range(32073)],
                'audioSamplerate': 16000
                }
        )

        self.assertEqual(response, {"data": {"voiceBelongsResident": True}})

    def test_accuracy_for_complete_false(self):
        response = self.client.execute(
            self.query,
            variables={
                'cpf': '0123456789',
                'audioSpeakingPhrase': [2.7 * x for x in range(32000)],
                'audioSpeakingName': [2.7 * x for x in range(32000)],
                'audioSamplerate': 16000
                }
        )

        self.assertEqual(response, {"data": {"voiceBelongsResident": False}})

    def test_accuracy_for_half_false(self):
        response = self.client.execute(
            self.query,
            variables={
                'cpf': '0123456789',
                'audioSpeakingPhrase': [x for x in range(32073)],
                'audioSpeakingName': [2.7 * x for x in range(32073)],
                'audioSamplerate': 16000
                }
        )

        self.assertEqual(response, {"data": {"voiceBelongsResident": False}})

    def test_nonexistent_cpf_except(self):
        response = self.client.execute(
            self.query,
            variables={
                'cpf': '1111111111',
                'audioSpeakingPhrase': [2.7 * x for x in range(32000)],
                'audioSpeakingName': [2.7 * x for x in range(32000)],
                'audioSamplerate': 16000
            }
        )

        self.assertIsNotNone(response['errors'])
