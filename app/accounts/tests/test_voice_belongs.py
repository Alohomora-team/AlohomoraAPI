import json
import pytest
from django.contrib.auth import get_user_model
from django.test import TestCase
from graphene.test import Client
from alohomora.schema import schema
import accounts.utility as Utility
from accounts.models import Resident
from graphql_jwt.testcases import JSONWebTokenTestCase
from scipy.io.wavfile import read
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
        self.residents = [
            'aline',
            'baraky',
            'felipe',
            'luis',
            'marcos',
            'mateus',
            'paulo',
            'pedro',
            'rodrigo',
            'samuel',
            'sergio',
            'silva',
            'victor',
            'vitor'
        ]

    def compute_accuracy(self, file_suffix):
        '''
        Calculate the "speaker identification" hit ratio for truly speakers (voice really belongs to resident)
        '''
        matches = 0.0
        for resident in  self.residents:
            samplerate, data = read('audios/' + resident + file_suffix)
            response = self.client.execute(
                self.query,
                variables={
                    'cpf': resident,
                    'audioSpeakingPhrase': data.tolist(),
                    'audioSamplerate': samplerate
                }
            )

            if response['data']['voiceBelongsResident'] == True:
                matches = matches + 1.0
        
        return matches / len(self.residents)

    def test_accuracy_for_clean_samples(self):
        '''
        Calculate hit ratio for clean audio samples
        '''
        hit_ratio = self.compute_accuracy('_clean.wav')
        
        # accuracy must be greater equal 85% 
        self.assertGreaterEqual(hit_ratio, 85.0)

    def test_accuracy_for_noised_samples(self):
        '''
        Calculate hit ratio for noised audio samples
        '''
        hit_ratio = self.compute_accuracy('_noised.wav')
        
        # accuracy must be greater equal 85% 
        self.assertGreaterEqual(hit_ratio, 85.0)

    def test_impostors_rejection(self):
        samplerate, data = read('audios/impostor.wav')
        rejections = 0.0
        for resident in self.residents:
            response = self.client.execute(
                self.query,
                variables={
                    'cpf': resident,
                    'audioSpeakingPhrase': data.tolist(),
                    'audioSamplerate': samplerate
                }
            )
            if response['data']['voiceBelongsResident'] == False:
                rejections = rejections + 1.0

        # accuracy must be greater equal 85% 
        self.assertGreaterEqual(rejections / len(self.residents), 85.0)

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
