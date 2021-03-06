"""
Tests of condos
"""

import pytest
from graphql_jwt.testcases import JSONWebTokenTestCase
from django.test import TestCase
from graphene.test import Client
from alohomora.schema import schema
from django.contrib.auth import get_user_model
from accounts.models import Service, Resident

@pytest.mark.usefixtures('test_data')
class ServiceTest(JSONWebTokenTestCase, TestCase):
    """Test that information can be retrieved and created using graphql"""

    def setUp(self):
        """Setup data for testing service"""

        self._client = Client(schema)
        self.super_user = get_user_model().objects.create_superuser(email='admin@example',
                                                                    password='123')
        self.client.authenticate(self.super_user)

    def test_create_service(self):
        """Test mutation createService"""

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

    def test_query_services(self):
        """Test query services"""

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

    def test_update_service(self):
        """Test mutation updateService"""

        self.user = get_user_model().objects.get(email='service@example.com')
        self.client.authenticate(self.user)

        mutation = '''
                    mutation {
                      updateService(serviceData: {serviceEmail: "service@example.com", email: "service2@exemplo.com", completeName: "k"}){
                        service {
                          email
                    	  	completeName
                        }
                      }
                    }
            '''
        result = self.client.execute(mutation)
        self.assertIsNone(result.errors)
        self.assertEqual(Resident.objects.count(), 1)
        self.assertDictEqual({"updateService": {
                                  "service": {
                                    "email": "service2@exemplo.com",
                                    "completeName": "k"
                                  }
                                }
                              }, result.data)

    def test_delete_service(self):
        """Test mutation deleteService"""

        mutation = '''
                    mutation{
                      deleteService(serviceEmail: "service@example.com")
                      {
                        serviceEmail
                      }
                    }
                            '''
        result = self.client.execute(mutation)
        self.assertIsNone(result.errors)
        self.assertEqual(Service.objects.count(), 0)
