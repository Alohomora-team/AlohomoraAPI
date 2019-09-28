from django.contrib.auth import get_user_model
from django.test import TestCase
from graphene.test import Client
from alohomora.schema import schema
from condos.models import Apartment, Block
import json

class GraphQLTestCase(TestCase):

    def setUp(self):
        self.user_object = get_user_model()
        self._client = Client(schema)

    def query(self, query: str):
        resp = self._client.execute(query)
        return resp

    def assertNoResponseErrors(self, resp: dict):
        self.assertNotIn('erros', resp, 'Response has erros')

    @classmethod
    def setUpTestData(cls):

        get_user_model().objects.create(
            complete_name='bob o construtor',
            email='charizard@exemplo.com',
            password='1231',
            cpf='12345678910',
            phone='42',
            voice_data=json.dumps([x for x in range(32000)]),
            admin=True
        )

        get_user_model().objects.create(
            complete_name='Sasuke Uchiha',
            email='sasuke@exemplo.com',
            password='itachi',
            cpf='12345111111',
            phone='42',
            voice_data=json.dumps([0 for i in range(32000)]),
            admin=True
        )

        get_user_model().objects.create(
            complete_name='Barry Allen',
            email='love_you_iris@exemplo.com',
            password='speedforce',
            cpf='11111111111',
            phone='42',
            voice_data=json.dumps([2 * x for x in range(32000)]),
            admin=True
        )

        get_user_model().objects.create(
            complete_name='Rock Lee do Pagode',
            email='lotus_primaria@exemplo.com',
            password='namorademais',
            cpf='99999999999',
            phone='42',
            voice_data=json.dumps([x**2 - 2*x + 3 for x in range(32000)]),
            admin=True
        )

    def test_mutation_user(self):

        block = Block.objects.create(number="1")
        Apartment.objects.create(number="101", block=block)

        mutation = '''
                mutation{
                  createUser(
                    completeName: "esquilo-voador",
                    email: "matpaulo@hoa",
                    password: "1231234",
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
        {
            users {
                id
                completeName
                email
                password
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
        self.assertEqual(data['users'][0]['password'], '1231')
        self.assertEqual(data['users'][0]['cpf'], '12345678910')
        self.assertEqual(data['users'][0]['phone'], '42')
        #Voice data nao pode ser comparado com valor inicial
        #self.assertEqual(data['users'][0]['voiceData'], json.dumps([x for x in range(32000)]))

    def test_query_voice_belongs_user(self):
        response = self.query(
            '''
            query voiceBelongsUser($cpf: String! , $voice_data: String!){
                voiceBelongsUser(cpf: $cpf, voice_data: $voice_data)
            }
            ''',
            op_name='voiceBelongsUser',
            variables={'cpf': '11111111111', 'voice_data': json.dumps([2 * x for x in range(32000)])}
        )

        content = json.loads(response)
        self.assertResponseNoErrors(response)
