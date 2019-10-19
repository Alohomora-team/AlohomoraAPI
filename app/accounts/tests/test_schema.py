import json
from django.contrib.auth import get_user_model
from django.test import TestCase
from graphene.test import Client
from alohomora.schema import schema
from condos.models import Apartment, Block
from accounts.models import Visitor, Resident, Service
import accounts.utility as Utility
from graphql_jwt.testcases import JSONWebTokenTestCase

class GraphQLTestCase(JSONWebTokenTestCase, TestCase):
    """Test that information can be retrieved and created using graphql"""
    maxDiff = None

    def setUp(self):
        self._client = Client(schema)
        self.user = get_user_model().objects.create(email='user@exemplo',
                                                    password='123',
                                                    username='user')
        self.super_user = get_user_model().objects.create_superuser(email='admin@exemplo',
                                                                    password='123')
        self.client.authenticate(self.super_user)

    def query(self, query: str):
        resp = self._client.execute(query)
        return resp

    def assertNoResponseErrors(self, resp: dict):
        self.assertNotIn('erros', resp, 'Response has erros')


    @classmethod
    def setUpTestData(cls):

        get_user_model().objects.create(
            email='service@example.com',
            password='service-password',
            username='service-username',
        )
        get_user_model().objects.create(
            email='resident@example.com',
            password='resident-password',
            username='resident-username',
        )

        block = Block.objects.create(number="1")
        apartment = Apartment.objects.create(number="101", block=block)
        Resident.objects.create(
            complete_name='resident-evil',
            password='resident-password',
            email='raccoon-city@exemplo.com',
            cpf='12345678910',
            phone='42',
            voice_data=json.dumps([x*10 for x in range(32000)]),
            admin=False,
            user=get_user_model().objects.get(email='resident@example.com'),
            apartment=apartment,
            block=block,
        )
        Visitor.objects.create(
            complete_name='bob o construtor',
            email='charizard@exemplo.com',
            cpf='12345678910',
            phone='42',
            voice_data='[[1],[2],[3]]',
        )
        Service.objects.create(
            complete_name='bob esponja',
            password='service-password',
            email='service@exemplo.com',
            user=get_user_model().objects.get(email='service@example.com'),
        )

    def test_mutation_resident(self):


        mutation = '''
                    mutation{
                      createResident(
                        completeName: "bob o construtor",
                        email: "resident@exemplo.com",
                        cpf: "12345678910",
                        phone: "42",
                        apartment: "101",
                        block: "1",
                        password: "resident",
                        mfccData: "[1,2,3]",
                        mfccAudioSpeakingName: "[1,2,3]"
                      ){ resident{
                         completeName
                         email
                         mfccAudioSpeakingName
                         voiceData
                      }
                      }
                    }
        '''

        result = self.client.execute(mutation)
        self.assertIsNone(result.errors)
        self.assertDictEqual({
            "createResident": {
                "resident": {
                    "completeName": "bob o construtor",
                    "email": "resident@exemplo.com",
                    "voiceData": "[1,2,3]",
                    "mfccAudioSpeakingName": "[1,2,3]"
                }
            }
        }, result.data)

    def test_query_residents(self):

        query = '''
                query{
                  residents{
                   completeName
                   email
                   phone
                   cpf
                  }
                }
        '''

        result = self.client.execute(query)
        self.assertIsNone(result.errors)
        self.assertDictEqual({
            "residents": [
                {
                    "completeName": "resident-evil",
                    "email": "raccoon-city@exemplo.com",
                    "phone": "42",
                    "cpf": "12345678910"
                }
            ]
        }, result.data)


    def test_query_resident_email(self):

        query = """
        {
            resident(email:"raccoon-city@exemplo.com"){
                completeName
            }
        }

        """

        result = self.client.execute(query)
        self.assertIsNone(result.errors)
        self.assertDictEqual({"resident":
                              {
                                  "completeName": "resident-evil"}
                             }, result.data)

    def test_query_resident_cpf(self):

        query = """
        {
            resident(cpf: "12345678910"){
                completeName
            }
        }

        """

        result = self.client.execute(query)
        self.assertIsNone(result.errors)
        self.assertDictEqual({"resident":
                              {
                                  "completeName": "resident-evil"}
                              }, result.data)


    def test_query_visitors(self):

        query = '''
                query{
                  visitors{
                   completeName
                   email
                   phone
                  }
                }
        '''

        result = self.client.execute(query)
        self.assertIsNone(result.errors)
        self.assertDictEqual({"visitors":
                              [{
                                  "completeName": "bob o construtor",
                                  "email": "charizard@exemplo.com",
                                  "phone": "42"}]
                              }, result.data)

    def test_mutation_visitors(self):

        mutation = '''
                        mutation {
                          createVisitor(completeName: "visitor", cpf: "123"
                          email: "oi@oi", phone: "123", voiceData: "[[1],[2],[3]]",, ownerCpf: "12345678910") {
                           visitor{
                            email
                            phone
                            completeName
                            cpf
                            owner {
                              completeName
                              cpf
                              email
                              phone
                              apartment {
                                number
                                      block {
                                		 	number
                              			}
                              }
                            }
                          }
                        }
                        }

        '''
        result = self.client.execute(mutation)
        self.assertIsNone(result.errors)
        self.assertDictEqual({
            "createVisitor": {
                "visitor": {
                    "email": "oi@oi",
                    "phone": "123",
                    "completeName": "visitor",
                    "cpf": "123",
                    "owner": {
                        "completeName": "resident-evil",
                        "cpf": "12345678910",
                        "email": "raccoon-city@exemplo.com",
                        "phone": "42",
                        "apartment": {
                            "number": "101",
                            "block": {
                                "number": "1"
                            }
                        }
                    }
                }
            }
        }, result.data)

    def test_query_services(self):

        query = '''
                    query {
                      services {
                        completeName
                        email
                      }
                    }
            '''
        result = self.client.execute(query)
        self.assertIsNone(result.errors)
        self.assertDictEqual({
            "services": [
                {
                    "completeName": "bob esponja",
                    "email": "service@exemplo.com"
                }
            ]
        }, result.data)

    def test_mutation_services(self):

        mutation = '''
                mutation{
                  createService(
                    completeName: "colheita-feliz",
                    email: "ibis@ni",
                    password: "123"
                  ){ service{
                     email
                     completeName
                  }
                  }
                }
        '''
        result = self.client.execute(mutation)
        self.assertIsNone(result.errors)
        self.assertDictEqual({
            "createService": {
                "service": {
                    "email": "ibis@ni",
                    "completeName": "colheita-feliz"
                }
            }
        }, result.data)
        self.assertNotEqual(get_user_model().objects.get(email="ibis@ni").password, '123')

    def test_authentication(self):

        self.client.authenticate(self.user)

        query = '''
                    query {
                      me {
                        username
                        email
                        password
                      }
                    }
            '''
        result = self.client.execute(query)
        self.assertIsNone(result.errors)
        self.assertDictEqual({"me":
                              {
                                  "username": "user",
                                  "email": "user@exemplo",
                                  "password": "123"}
                             }, result.data)

class VoiceBelongsUserTests(TestCase):
    """Test using mfcc and fastwd for voice recognition and authentication"""

    def setUp(self):
        self.client = Client(schema)
        self.query = '''
        query voiceBelongsResident($cpf: String!, $voice_data: String!)
            {
                voiceBelongsResident(cpf: $cpf, voiceData: $voice_data )
            }
        '''

    @classmethod
    def setUpTestData(cls):
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
            voice_data=Utility.json_voice_data_to_json_mfcc(
                json.dumps([2 * x for x in range(32000)])
            ),
        )

        Resident.objects.create(
            complete_name="Naruto Uzumaku",
            email="sereihokage@konoha.com",
            phone="6133941597",
            cpf="0123456781",
            user=get_user_model().objects.get(email='resident2@example.com'),
            voice_data=Utility.json_voice_data_to_json_mfcc(
                json.dumps([3 * x for x in range(32000)])
            ),
        )

        Resident.objects.create(
            complete_name="Max Steel",
            email="modoturbo@yahoo.com",
            phone="6133941596",
            cpf="0123456782",
            user=get_user_model().objects.get(email='resident3@example.com'),
            voice_data=Utility.json_voice_data_to_json_mfcc(
                json.dumps([x**2  - 50 * x + 20 for x in range(32000)])
            ),
        )

        Resident.objects.create(
            complete_name="Benjamin Tennyson",
            email="ben10@omnitrix.com",
            phone="33941595",
            cpf="0123456783",
            user=get_user_model().objects.get(email='resident4@example.com'),
            voice_data=Utility.json_voice_data_to_json_mfcc(
                json.dumps([x - 200 for x in range(32000)])
            ),
        )

        Resident.objects.create(
            complete_name="Eren Jaeger",
            email="i_hate_marleyans@eldia.com",
            phone="99999999",
            cpf="0000000000",
            user=get_user_model().objects.get(email='resident5@example.com'),
            voice_data=Utility.json_voice_data_to_json_mfcc(
                json.dumps([x * 0.5 for x in range(32000)])
            ),
        )

    def test_query_accuracy_true(self):
        response = self.client.execute(
            self.query,
            variables={
                'cpf': '0123456789',
                'voice_data': json.dumps([2.3 * x for x in range(32000)])
                }
        )

        self.assertEqual(response, {"data": {"voiceBelongsResident": True}})

    def test_query_accuracy_false(self):
        response = self.client.execute(
            self.query,
            variables={
                'cpf': '0123456789',
                'voice_data': json.dumps([2.7 * x for x in range(32000)])
                }
        )

        self.assertEqual(response, {"data": {"voiceBelongsResident": False}})

    def test_nonexistent_cpf_except(self):
        response = self.client.execute(
            self.query,
            variables={
                'cpf': '1111111111',
                'voice_data': json.dumps([2.3 * x for x in range(32000)])
            }
        )

        self.assertIsNotNone(response['errors'])

    def test_invalid_voice_data(self):
        response = self.client.execute(
            self.query,
            variables={
                'cpf': '0123456789',
                'voice_data': json.dumps([2.3 * x for x in range(32000)] + ['a'])
            }
        )

        self.assertIsNotNone(response['errors'])
