import json
from django.contrib.auth import get_user_model
from django.test import TestCase
from graphene.test import Client
from alohomora.schema import schema
from condos.models import Apartment, Block
from accounts.models import User, Visitor
import accounts.utility as Utility
from graphql_jwt.testcases import JSONWebTokenTestCase

class GraphQLTestCase(JSONWebTokenTestCase, TestCase):

    def setUp(self):
        self.user_object = User
        self._client = Client(schema)
        self.service = get_user_model().objects.create(email='chazard@exemplo',
                                                       password='12',
                                                       username='service')

    def query(self, query: str):
        resp = self._client.execute(query)
        return resp

    def assertNoResponseErrors(self, resp: dict):
        self.assertNotIn('erros', resp, 'Response has erros')


    @classmethod
    def setUpTestData(cls):

        User.objects.create(
            complete_name='bob o construtor',
            email='charizard@exemplo.com',
            cpf='12345678910',
            phone='42',
            voice_data=json.dumps([x*10 for x in range(32000)]),
            admin=True
        )
        Visitor.objects.create(
            complete_name='bob o construtor',
            email='charizard@exemplo.com',
            cpf='12345678910',
            phone='42',
            voice_data='Singing in the Rain',
        )

    def test_mutation_user(self):

        block = Block.objects.create(number="1")
        Apartment.objects.create(number="101", block=block)

        mutation = '''
                mutation{
                  createUser(
                    completeName: "esquilo-voador",
                    email: "matpaulo@hoa",
                    cpf: "12345678911",
                    phone: "11123",
                    apartment: "101",
                    block: "1",
                    voiceData: "[[1],[2],[3]]",
                  ){ user{
                     completeName
                     email
                     cpf
                     phone
                     voiceData
                     apartment{
                        number
                        block{
                            number
                        }
                     }
                  }
                  }
                }
        '''

        response = self.query(query=mutation)
        self.assertNoResponseErrors(response)
        data = list(list(list(response['data'].items())[0][1].items())[0][1].items())

        self.assertEqual(data[0][1], "esquilo-voador")
        self.assertEqual(data[1][1], "matpaulo@hoa")
        self.assertEqual(data[2][1], "12345678911")
        self.assertEqual(data[3][1], "11123")
        # voice_data não pode ser comparado com valor incial
        #self.assertEqual(data[4][1], "[[1],[2],[3]]")
        self.assertEqual(list(data[5][1].items())[0][1], "101")
        self.assertEqual(list(list(data[5][1].items())[1][1].items())[0][1], "1")

    def test_query_users(self):

        query = '''
                query{
                  users{
                   id
                   completeName
                   email
                   phone
                   cpf
                   voiceData
                  }
                }
        '''

        response = self._client.execute(query)
        data = response['data']
        self.assertEqual(len(data), 1)
        self.assertEqual(data['users'][0]['completeName'], 'bob o construtor')
        self.assertEqual(data['users'][0]['email'], 'charizard@exemplo.com')
        self.assertEqual(data['users'][0]['cpf'], '12345678910')
        self.assertEqual(data['users'][0]['phone'], '42')
        #Voice data nao pode ser comparado com valor inicial
        #self.assertEqual(data['users'][0]['voiceData'], json.dumps([x for x in range(32000)]))


    def test_query_user_email(self):

        query = """
        {
            user(email: "charizard@exemplo.com"){
                completeName
            }
        }

        """

        response = self._client.execute(query)
        data = response['data']
        self.assertEqual(data['user']['completeName'], 'bob o construtor')

    def test_query_user_cpf(self):

        query = """
        {
            user(cpf: "12345678910"){
                completeName
            }
        }

        """

        response = self._client.execute(query)
        data = response['data']
        self.assertEqual(data['user']['completeName'], 'bob o construtor')


    def test_query_visitors(self):

        query = '''
                query{
                  visitors{
                   id
                   completeName
                   email
                   cpf
                   phone
                   voiceData
                  }
                }
        '''

        response = self.query(query=query)
        data = response['data']
        self.assertEqual(len(data), 1)
        self.assertEqual(data['visitors'][0]['completeName'], 'bob o construtor')
        self.assertEqual(data['visitors'][0]['email'], 'charizard@exemplo.com')
        self.assertEqual(data['visitors'][0]['cpf'], '12345678910')
        self.assertEqual(data['visitors'][0]['phone'], '42')
        self.assertEqual(data['visitors'][0]['voiceData'], 'Singing in the Rain')

    def test_query_services(self):

        query = '''
                query {
                  services {
                    id
                    username
                    email
                    password
                  }
                }
                '''

        response = self.query(query=query)
        data = response['data']
        self.assertEqual(len(data), 1)
        self.assertEqual(data['services'][0]['username'], 'service')
        self.assertEqual(data['services'][0]['email'], 'chazard@exemplo')
        self.assertEqual(data['services'][0]['password'], '12')

    def test_mutation_services(self):

        mutation = '''
                        mutation{
                          createService(
                            username: "colheita-feliz",
                            email: "ibis@ni",
                            password: "123"
                          ){ service{
                             username
                             email
                             password
                          }
                          }
                        }
        '''
        response = self.query(query=mutation)
        self.assertNoResponseErrors(response)
        self.assertEqual(get_user_model().objects.count(), 2)
        self.assertEqual(get_user_model().objects.get(email="ibis@ni").username, 'colheita-feliz')
        self.assertEqual(get_user_model().objects.get(email="ibis@ni").email, 'ibis@ni')
        self.assertNotEqual(get_user_model().objects.get(email="ibis@ni").password, '123')

    def test_authentication(self):

        self.service.set_password('12')

        self.client.authenticate(self.service)

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
                                  "username": "service",
                                  "email": "chazard@exemplo",
                                  "password": "12"}
                             }, result.data)
class VoiceBelongsUserTests(TestCase):

    def setUp(self):
        self.client = Client(schema)
        self.query = '''
        query voiceBelongsUser($cpf: String!, $voice_data: String!)
            {
                voiceBelongsUser(cpf: $cpf, voiceData: $voice_data )
            }
        '''

    @classmethod
    def setUpTestData(cls):
        User.objects.create(
            complete_name="Barry Allen",
            email="love_you_iris@starslab.com",
            phone="6133941598",
            cpf="0123456789",
            voice_data=Utility.json_voice_data_to_json_mfcc(
                json.dumps([2 * x for x in range(32000)])
            ),
        )

        User.objects.create(
            complete_name="Naruto Uzumaku",
            email="sereihokage@konoha.com",
            phone="6133941597",
            cpf="0123456781",
            voice_data=Utility.json_voice_data_to_json_mfcc(
                json.dumps([3 * x for x in range(32000)])
            ),
        )

        User.objects.create(
            complete_name="Max Steel",
            email="modoturbo@yahoo.com",
            phone="6133941596",
            cpf="0123456782",
            voice_data=Utility.json_voice_data_to_json_mfcc(
                json.dumps([x**2  - 50 * x + 20 for x in range(32000)])
            ),
        )

        User.objects.create(
            complete_name="Benjamin Tennyson",
            email="ben10@omnitrix.com",
            phone="33941595",
            cpf="0123456783",
            voice_data=Utility.json_voice_data_to_json_mfcc(
                json.dumps([x - 200 for x in range(32000)])
            ),
        )

        User.objects.create(
            complete_name="Eren Jaeger",
            email="i_hate_marleyans@eldia.com",
            phone="99999999",
            cpf="0000000000",
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

        self.assertEqual(response, {"data": {"voiceBelongsUser": True}})

    def test_query_accuracy_false(self):
        response = self.client.execute(
            self.query,
            variables={
                'cpf': '0123456789',
                'voice_data': json.dumps([2.7 * x for x in range(32000)])
                }
        )

        self.assertEqual(response, {"data": {"voiceBelongsUser": False}})

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
