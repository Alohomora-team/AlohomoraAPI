import json
import pytest
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

@pytest.mark.usefixtures('test_voice_data')
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
