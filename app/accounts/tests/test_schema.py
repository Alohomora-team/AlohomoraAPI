from django.contrib.auth import get_user_model
from django.test import TestCase
from graphene.test import Client
from alohomora.schema import schema
from condos.models import Apartment, Block
from accounts.models import User, Visitor
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
            voice_data='Singing in the Rain',
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
        self.assertEqual(data['users'][0]['voiceData'], 'Singing in the Rain')


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

    def test_mutation_visitor(self):

        mutation = '''
            mutation {
              createVisitor(
                completeName: "visitor",
                cpf: "1234567893"
                email: "visitor@",
                phone: "123",
                voiceData: "visitor is singing",
                ownerCpf: "12345678910") {
                    owner {
                      completeName
                      cpf
                    }
              }
            }

        '''

        response = self.query(query=mutation)
        self.assertNoResponseErrors(response)
        self.assertEqual(Visitor.objects.count(), 2)
        self.assertEqual(Visitor.objects.get(phone="123").email, 'visitor@')
        self.assertEqual(Visitor.objects.get(phone="123").phone, '123')
        self.assertEqual(Visitor.objects.get(phone="123").complete_name, 'visitor')
        self.assertEqual(Visitor.objects.get(phone="123").cpf, '1234567893')
        self.assertEqual(Visitor.objects.get(phone="123").voice_data, 'visitor is singing')
        self.assertEqual(Visitor.objects.get(phone="123").owner.cpf, '12345678910')
        self.assertEqual(Visitor.objects.get(phone="123").owner.complete_name, 'bob o construtor')

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
