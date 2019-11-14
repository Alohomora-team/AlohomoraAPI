"""
Tests of user
"""

import pytest
from graphql_jwt.testcases import JSONWebTokenTestCase
from django.test import TestCase
from graphene.test import Client
from alohomora.schema import schema
from django.contrib.auth import get_user_model
from accounts.models import Resident

@pytest.mark.usefixtures('test_data')
class UserTest(JSONWebTokenTestCase, TestCase):
    """Test that information can be retrieved and created using graphql"""

    def setUp(self):
        """Setup data for testing user"""

        self._client = Client(schema)
        self.user = get_user_model().objects.create(email='user@example',
                                                    password='123',
                                                    username='user',
                                                    is_active=True,)
        self.super_user = get_user_model().objects.create_superuser(email='admin@example',
                                                                    password='123')
        self.client.authenticate(self.super_user)

    def test_query_users(self):
        """Test query users"""

        query = '''
                query{
                  users{
                   email
                  }
                }
        '''
        result = self.client.execute(query)
        self.assertIsNone(result.errors)
        self.assertDictEqual({"users": [
                              {"email": "creator@example.com"},
                              {"email": "admin2@example.com"},
                              {"email": "service@example.com"},
                              {"email": "resident@example.com"},
                              {"email": "desativado@example.com"},
                              {"email": "user@example"},
                              {"email": "admin@example"},
                            ]
                  }, result.data)

    def test_query_unactive_users(self):
        """Test query unactivesUsers"""

        query = '''
                    query {
                      unactivesUsers {
                        username
                      }
                    }
            '''
        result = self.client.execute(query)
        self.assertIsNone(result.errors)
        self.assertDictEqual({
            "unactivesUsers": [
                {
                    "username": "desativado-username"
                }
            ]
        }, result.data)

    def test_authentication(self):
        """Test query me"""

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
                                  "email": "user@example",
                                  "password": "123"}
                             }, result.data)

    def test_deactivated_user(self):
        """Test mutation deactivateUser"""

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
        self.user = get_user_model().objects.get(email="resident@example.com")
        with self.assertRaises(Exception):
            self.client.authenticate(self.user)
            mutation = '''
                    mutation {
                      createVisitor(completeName: "visitor2", cpf: "40982705018") {
                       visitor{
                        id
                        completeName
                        cpf
                      }
                    }
                    }
                '''
            result = self.client.execute(mutation)
            self.assertIsNone(result.errors)
    def test_activated_user(self):
        """Test mutation activateUser"""

        mutation = '''
                    mutation{
                      activateUser(
                        userEmail: "resident@example.com",)
                      { user{
                           isActive
                      }
                      }
                    }
            '''
        result = self.client.execute(mutation)
        self.assertIsNone(result.errors)
        mutation = '''
                    mutation {
                      createVisitor(completeName: "visitor2", cpf: "40982705018") {
                       visitor{
                        id
                        completeName
                        cpf
                      }
                    }
                    }
            '''
        result = self.client.execute(mutation)
        self.assertIsNone(result.errors)
