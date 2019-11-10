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
        self._client = Client(schema)
        self.super_user = get_user_model().objects.create_superuser(email='admin@example',
                                                                    password='123')
        self.client.authenticate(self.super_user)

    def test_mutation_resident(self):


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
                    "email": "resident2@example.com",
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

    def test_update_resident(self):

        self.user = get_user_model().objects.get(email='resident@example.com')
        self.client.authenticate(self.user)
        mutation = '''
mutation {
  updateResident(residentData: {email: "service42@example.com", password: "k"}){
    resident {
      email
      completeName
      phone
    }
    user {
      	email
      }
  }
}
            '''
        result = self.client.execute(mutation)
        self.assertIsNone(result.errors)
        self.assertEqual(Resident.objects.count(), 1)

        self.assertDictEqual({"updateResident":
                              {
                                  "resident": {
                                      "email": "service42@example.com",
                                      "completeName": "resident-evil",
                                      "phone": "42"},
                                  "user": {
                                      "email": "service42@example.com",}
                                  }
                              }, result.data)

    def test_delete_resident(self):

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
