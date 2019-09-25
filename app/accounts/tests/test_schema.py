from django.contrib.auth import get_user_model
from django.test import TestCase
from graphene.test import Client
from alohomora.schema import schema

class GraphQLTestCase(TestCase):

    def setUp(self):
        self.user_object = get_user_model()
        self._client = Client(schema)

    @classmethod
    def setUpTestData(cls):

        user = get_user_model().objects.create(
            complete_name='bob o construtor',
            email='charizard@exemplo.com',
            password='1231',
            cpf='12345678910',
            phone='42',
            voice_data='Singing in the Rain',
            admin=True
        )
     
    def test_mutation_user(self):

        mutation = '''mutation {
                        createUser(
                            completeName:"felipe",
                            email: "felipeborges@gmail.com",
                            password: "1234",
                            cpf: "1234",
                            phone: "234123",
                            block: "1",
                            apartment : "40",
                            voiceData: "asdfa"){
                            user{
                              completeName
                              email
                              cpf
                              phone
                              voiceData
                            }
                        }
                      }
            '''

        response = self._client.execute(mutation)
        user = self.user_object.objects.get(email='felipeborges@gmail.com')
        self.assertEqual(user.cpf, "1234")
        self.assertEqual(user.phone, "234123")
        self.assertEqual(user.voice_data, "asdfa")
        self.assertEqual(user.complete_name, "felipe")

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
        self.assertEqual(data['users'][0]['voiceData'], 'Singing in the Rain')
