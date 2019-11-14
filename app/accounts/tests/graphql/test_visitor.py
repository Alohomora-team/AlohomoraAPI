"""
Tests of condos
"""

import pytest
from graphql_jwt.testcases import JSONWebTokenTestCase
from django.test import TestCase
from graphene.test import Client
from alohomora.schema import schema
from django.contrib.auth import get_user_model
from accounts.models import Visitor

@pytest.mark.usefixtures('test_data')
class VisitorTest(JSONWebTokenTestCase, TestCase):
    """Test that information can be retrieved and created using graphql"""

    def setUp(self):
        """Setup data for testing visitor"""

        self._client = Client(schema)
        self.super_user = get_user_model().objects.create_superuser(email='admin@example',
                                                                    password='123')
        self.client.authenticate(self.super_user)

    def test_query_visitors(self):
        """Test query visitors"""

        query = '''
                    query{
                      allVisitors{
                       completeName
                       cpf
                      }
                    }
        '''

        result = self.client.execute(query)
        self.assertIsNone(result.errors)
        self.assertDictEqual({"allVisitors": [
                                  {
                                    "completeName": "visitor",
                                    "cpf": "29950509041"
                                  }
                                ]
                              }, result.data)

    def test_create_visitor(self):
        """Test mutation createVisitor"""

        mutation = '''
                    mutation {
                      createVisitor(completeName: "visitor2", cpf: "40982705018") {
                       visitor{
                        completeName
                        cpf
                      }
                    }
                    }
        '''
        result = self.client.execute(mutation)
        self.assertIsNone(result.errors)
        self.assertDictEqual({
    "createVisitor": {
      "visitor": {
        "completeName": "visitor2",
        "cpf": "40982705018"
      }
    }
  }, result.data)

    def test_update_visitor(self):
        """Test mutation createVisitor"""

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

        mutation = '''
                    mutation {
                      updateVisitor(cpf: "40982705018", newCpf:"80272869058"){
                        visitor{
                          cpf
                          completeName
                        }
                      }
                    }
              '''
        result = self.client.execute(mutation)
        self.assertIsNone(result.errors)
        self.assertDictEqual({"updateVisitor":
                              {
                                  "visitor": {
                                    "cpf": "80272869058",
                                    "completeName": "visitor2"
                                  }
                                }
                              }, result.data)

    def test_delete_visitor(self):
       """Test mutation deleteVisitor"""

       mutation = '''
                  mutation{
                    deleteVisitor(cpf: "29950509041")
                    {
                    	cpf
                    }
                  }
                  '''
       result = self.client.execute(mutation)
       self.assertIsNone(result.errors)
       self.assertEqual(Visitor.objects.count(), 0)
