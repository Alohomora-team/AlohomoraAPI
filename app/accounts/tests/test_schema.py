from django.contrib.auth import get_user_model
from django.test import TestCase
from graphene.test import Client
from alohomora.schema import schema
from condos.models import Apartment, Block


# ========== utility function ==========

def create_test_user(**kwargs):


    user = get_user_model().objects.create(complete_name='bob o construtor',
                                           email='charizard@exemplo.com',
                                           password='1231',
                                           cpf='12345678910',
                                           phone='42',
                                           voice_data='Singing in the Rain',
                                           admin=True)
    return user

# ========== createUser mutation tests ==========

class GraphQLTestCase(TestCase):
    def setUp(self):
        self._client = Client(schema)
    def query(self, query: str):
        resp = self._client.execute(query)
        return resp
    def assertNoResponseErrors(self, resp: dict):
        self.assertNotIn('errors', resp, 'Response has errors')

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
                    voiceData: "11ok",
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
        self.assertEqual(data[4][1], "11ok")
        self.assertEqual(list(data[5][1].items())[0][1], "101")
        self.assertEqual(list(list(data[5][1].items())[1][1].items())[0][1], "1")

# ========== createUser query tests ==========

    def test_query_users(self):
        user = create_test_user()

        user.save()
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
        response = self.query(query=query)
        self.assertNoResponseErrors(response)
        data = response['data']
        self.assertEqual(len(data), 1)
        self.assertEqual(data['users'][0]['completeName'], 'bob o construtor')
        self.assertEqual(data['users'][0]['email'], 'charizard@exemplo.com')
        self.assertEqual(data['users'][0]['password'], '1231')
        self.assertEqual(data['users'][0]['cpf'], '12345678910')
        self.assertEqual(data['users'][0]['phone'], '42')
        self.assertEqual(data['users'][0]['voiceData'], 'Singing in the Rain')
