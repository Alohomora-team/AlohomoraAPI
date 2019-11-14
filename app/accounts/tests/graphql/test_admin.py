"""
Tests of admins
"""
import pytest
from graphql_jwt.testcases import JSONWebTokenTestCase
from django.test import TestCase
from graphene.test import Client
from alohomora.schema import schema
from django.contrib.auth import get_user_model
from accounts.models import Admin

@pytest.mark.usefixtures('test_data')
class GraphQLTestCase(JSONWebTokenTestCase, TestCase):
    """Test that information can be retrieved and created using graphql"""


    def setUp(self):
        self._client = Client(schema)
        self.user = get_user_model().objects.create(email='user@example',
                                                    password='123',
                                                    username='user',
                                                    is_active=True,)

        self.super_user = get_user_model().objects.create_superuser(email='admin@example',
                                                                    password='123')

        self.admin = Admin.objects.create(
                admin=self.user,
                creator=self.super_user
            )

        self.client.authenticate(self.super_user)


    def test_mutation_createAdmin(self):
        mutation = '''
                    mutation{
                      createAdmin(
                        email: "admin3@example.com",
                        password: "admin3-password"
                      ){
                        email
                      }
                    }
        '''

        result = self.client.execute(mutation)
        self.assertIsNone(result.errors)
        self.assertDictEqual({
            "createAdmin": {
                "email": "admin3@example.com"
            }
        }, result.data)

    def test_mutation_deleteAdmin(self):
        mutation = '''
                    mutation{
                      deleteAdmin(email: "user@example"){
                        email
                      }
                    }
        '''

        result = self.client.execute(mutation)
        self.assertIsNone(result.errors)
        self.assertDictEqual({
            "deleteAdmin": {
                "email": "user@example"
            }
        }, result.data)

    def test_query_all_admins(self):
        query = '''
                query{
                  allAdmins{
                    admin{
                      email
                    }
                  }
                }
        '''
        result = self.client.execute(query)
        self.assertIsNone(result.errors)
        self.assertDictEqual({
            "allAdmins": [
                {
                  "admin": {
                    "email": "user@example"
                  }
                }
            ]
        }, result.data)

    def test_query_admin(self):
        query = '''
                query{
                  admin(adminEmail:"user@example"){
                    admin{
                      email
                    }
                  }
                }
        '''
        result = self.client.execute(query)
        self.assertIsNone(result.errors)
        self.assertDictEqual({
            "admin": [
                {
                  "admin": {
                    "email": "user@example"
                  }
               }
            ]
        }, result.data)
