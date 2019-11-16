"""
Tests of resident
"""

import pytest
from graphql_jwt.testcases import JSONWebTokenTestCase
from django.test import TestCase
from graphene.test import Client
from alohomora.schema import schema
from django.contrib.auth import get_user_model
from accounts.models import Resident

@pytest.mark.usefixtures('test_data')
class ResidentTest(JSONWebTokenTestCase, TestCase):
    """Test that information can be retrieved and created using graphql"""

    def setUp(self):
        """Setup for testing resident"""

        self._client = Client(schema)
        self.super_user = get_user_model().objects.create_superuser(email='admin@example',
                                                                    password='123')
        self.client.authenticate(self.super_user)

    def test_mutation_resident(self):
        """Test mutation createResident"""


        mutation = '''
                    mutation{
                      createResident(
                        completeName: "bob o construtor",
                        email: "resident2@example.com",
                        cpf: "12345678910",
                        phone: "42",
                        apartment: "101",
                        block: "1",
                        password: "resident",
                        audioSpeakingPhrase: [1.0, 2.0, 3.0, 4.0, 5.0],
                        audioSpeakingName: [1.0, 2.0, 3.0, 4.0, 5.0]
                      ){ resident{
                         completeName
                         email
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
                    "email": "resident2@example.com"
                }
            }
        }, result.data)

    def test_query_residents(self):
        """Test query residents"""

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
        """Test query resident email"""

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
        """Test query resident cpf"""

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

    def test_update_resident(self):
        """Test mutation updateResident"""

        mutation = '''
                    mutation {
                      updateResident(residentData: {residentCpf: "12345678910", cpf: "00012312300", completeName: "k"}){
                        resident {
                          cpf
                    	  	completeName
                        }
                      }
                    }
              '''
        result = self.client.execute(mutation)
        self.assertIsNone(result.errors)
        self.assertDictEqual({"updateResident": {
                                  "resident": {
                                    "cpf": "00012312300",
                                    "completeName": "k"
                                  }
                                }
                              }, result.data)

    def test_delete_resident(self):
        """Test mutation deleteResident"""

        mutation = '''
                    mutation{
                      deleteResident(residentEmail: "resident@example.com")
                      {
                        residentEmail
                      }
                    }
                            '''
        result = self.client.execute(mutation)
        self.assertIsNone(result.errors)
        self.assertEqual(Resident.objects.count(), 0)
