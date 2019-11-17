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
    maxDiff = None

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
        self.assertEqual(get_user_model().objects.count(), 7)

    def test_mutation_user(self):
        """Test mutation createUser"""

        mutation = '''
                    mutation{
                      createUser(
                        username: "service",
                        email: "service@exemplo.com",
                        password: "123"
                      ){ user{
                         username
                         email
                      }
                      }
                    }
        '''

        result = self.client.execute(mutation)
        self.assertIsNone(result.errors)
        self.assertDictEqual({"createUser": {
                                  "user": {
                                    "username": "service",
                                    "email": "service@exemplo.com"
                                  }
                                }
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

    def test_authentication_error(self):
        """Test error on authentication"""

        mutation = '''
                    mutation{
                      createUser(
                        username: "goten",
                        email: "goten@example.com",
                        password: "123"
                      ){ user{
                         username
                         email
                      }
                      }
                    }
        '''
        self.client.execute(mutation)
        self.user.is_active = True
        self.user=get_user_model().objects.get(email="goten@example.com")
        result = self.client.authenticate(self.user)
        query = '''
                    query {
                      me {
                        username
                        email
                      }
                    }
            '''
        result = self.client.execute(query)
        self.assertIsNotNone(result.errors)
        self.user.is_active = True
        self.user.save()
        self.client.authenticate(self.user)
        result = self.client.execute(query)
        self.assertIsNone(result.errors)

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

    def test_changing_email(self):
        """Test mutation changeEmail"""

        mutation = '''
                    mutation{
                      changeEmail(userEmail: "service@example.com", email: "gohan@example.com"){
                        user{
                           email
                      	}
                      }
                    }
        '''

        result = self.client.execute(mutation)
        self.assertIsNone(result.errors)
        self.assertDictEqual({"changeEmail": {
                                  "user": {
                                    "email": "gohan@example.com"
                                  }
                                }
                              }, result.data)

    def test_changing_password(self):
        """Test mutation changePassword"""

        mutation = '''
                    mutation{
                      changePassword(userEmail: "service@example.com", password: "123"){
                        user{
                           password
                      	}
                      }
                    }
        '''

        result = self.client.execute(mutation)
        self.assertIsNone(result.errors)
