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
                                                    username='user',
                                                    is_active=True,)
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
            is_active=True,
            is_service=True,
        )
        get_user_model().objects.create(
            email='resident@example.com',
            password='resident-password',
            username='resident-username',
            is_active=True,
            is_resident=True,
        )

        block = Block.objects.create(number="1")
        apartment = Apartment.objects.create(number="101", block=block)
        Resident.objects.create(
            complete_name='resident-evil',
            password='resident-password',
            email='resident@example.com',
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
            email='service@example.com',
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
                    "email": "resident@example.com",
                    "phone": "42",
                    "cpf": "12345678910"
                }
            ]
        }, result.data)


    def test_query_resident_email(self):

        query = """
        {
            resident(email:"resident@example.com"){
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
                        "email": "resident@example.com",
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
                    "email": "service@example.com"
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
    def test_deactivated_user(self):
        mutation = '''
                    mutation{
                      deactivateUser(
                        userEmail: "resident@example.com",)
                      { user{
                           isActive
                      }
                      }
                    }
            '''
        result = self.client.execute(mutation)
        self.assertIsNone(result.errors)
        get_user_model().objects.get(is_resident=True)
        with self.assertRaises(Exception):
            self.client.authenticate(self.user)
            mutation = '''
                            mutation {
                              createVisitor(completeName: "visitor", cpf: "123"
                              email: "oi@oi", phone: "123", voiceData: "[[1],[2],[3]]",, ownerCpf: "12345678910") {
                               visitor{
                                email
                              }
                            }
                            }

                '''
            result = self.client.execute(mutation)
            self.assertIsNone(result.errors)
