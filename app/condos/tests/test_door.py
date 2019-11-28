"""
Tests of condos
"""

from graphene.test import Client
from django.test import TestCase
from django.contrib.auth import get_user_model
from condos.models import Apartment, Block
from alohomora.schema import schema
from graphql_jwt.testcases import JSONWebTokenTestCase

"""
Tests of condos
"""

from graphene.test import Client
from django.test import TestCase
from django.contrib.auth import get_user_model
from condos.models import Apartment, Block
from alohomora.schema import schema
from graphql_jwt.testcases import JSONWebTokenTestCase

class GraphQLTestCase(JSONWebTokenTestCase, TestCase):
    """Test that information can be retrieved and created using graphql"""

    def setUp(self):
        """Setup data for testing doors"""

        self._client = Client(schema)

    def test_door_mutation(self):
        """Test mutation updateDoor"""

        mutation = '''
                        mutation {
                          updateDoor(enter: true){
                            enter
                          }
                        }
        '''

        result = self.client.execute(mutation)
        self.assertIsNone(result.errors)
        self.assertDictEqual({"updateDoor": {
                                  "enter": True
                                }
                              }, result.data)
    def test_door_query(self):
        """Test query door"""

        mutation = '''
                        query {
                          door
                        }
        '''

        result = self.client.execute(mutation)
        self.assertIsNone(result.errors)
        self.assertDictEqual({"door": True}, result.data)
