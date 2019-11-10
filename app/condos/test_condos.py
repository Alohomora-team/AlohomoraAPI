from graphene.test import Client
from django.test import TestCase
from django.contrib.auth import get_user_model
from condos.models import Apartment, Block
from alohomora.schema import schema
from graphql_jwt.testcases import JSONWebTokenTestCase

class GraphQLTestCase(JSONWebTokenTestCase, TestCase):
    """Test that information can be retrieved and created using graphql"""

    def setUp(self):
        self._client = Client(schema)
        block = Block.objects.create(number="1")
        Apartment.objects.create(number="101", block=block)
        self.super_user = get_user_model().objects.create_superuser(email='admin@exemplo',
                                                                    password='123')
        self.client.authenticate(self.super_user)

    def query(self, query: str):
        resp = self._client.execute(query)
        return resp

    def test_block_mutation(self):

        mutation = '''
                        mutation{
                          createBlock(number: "2"){
                          number
                          }
                        }
        '''

        result = self.client.execute(mutation)
        self.assertIsNone(result.errors)
        self.assertDictEqual({"createBlock":
                              {
                                  "number": "2"}
                              }, result.data)

    def test_block_query(self):

        query = """
        {
            block(number:"1"){
                number
            }
        }
        """

        result = self.client.execute(query)
        self.assertIsNone(result.errors)
        self.assertDictEqual({"block":
                              {
                                  "number": "1"}
                             }, result.data)

    def test_apartment_mutation(self):

        mutation = '''
                        mutation{
                          createApartment(blockNumber: "1", number: "102"
                          ){
                             number
                             block{
                              number
                            }
                          }
                        }
        '''

        result = self.client.execute(mutation)
        self.assertIsNone(result.errors)
        self.assertDictEqual({"createApartment":
                              {
                                  "number": "102",
                                  "block": {
                                      "number": "1"}
                              }
                             }, result.data)

    def test_apartment_query(self):

        query = """
        {
            apartment(number:"101", block: "1"){
                number
                block{
                    number
                }
            }
        }
        """

        result = self.client.execute(query)
        self.assertIsNone(result.errors)
        self.assertDictEqual({"apartment":
                              {
                                  "number": "101",
                                  "block": {
                                      "number": "1"}
                              }
                              }, result.data)

    def test_apartments_query(self):

        query = """
        {
            apartments(number:"101"){
                number
                block{
                    number
                }
            }
        }
        """

        result = self.client.execute(query)
        self.assertIsNone(result.errors)
        self.assertDictEqual({"apartments":
                              [{
                                  "number": "101",
                                  "block": {
                                      "number": "1"}
                              }]
                              }, result.data)

    def test_delete_apartment(self):
        mutation = '''
                        mutation{
                          deleteApartment(apartmentNumber: 101)
                          {
                            apartmentNumber
                          }
                        }
                            '''
        result = self.client.execute(mutation)
        self.assertIsNone(result.errors)
        self.assertEqual(Apartment.objects.count(), 0)

    def test_delete_block(self):
        mutation = '''
                        mutation{
                          deleteBlock(blockNumber: "1")
                          {
                            blockNumber
                          }
                        }
                            '''
        result = self.client.execute(mutation)
        self.assertIsNone(result.errors)
        self.assertEqual(Block.objects.count(), 0)

    def test_update_block(self):
        mutation = '''
                    mutation {
                      updateBlock(number: "2", blockNumber: "1"){
                        block {
                          number
                        }
                      }
                    }
                            '''
        result = self.client.execute(mutation)
        self.assertIsNone(result.errors)
        self.assertDictEqual({"updateBlock":
                              {
                                  "block": {
                                      "number": "2"}
                                  }
                              }, result.data)

    def test_update_apartment(self):
        mutation = '''
                        mutation {
                          updateApartment(number: "202", apartmentNumber: "101"){
                            apartment {
                              number
                            }
                          }
                        }
                            '''
        result = self.client.execute(mutation)
        self.assertIsNone(result.errors)
        self.assertEqual(Block.objects.count(), 1)
        self.assertDictEqual({"updateApartment":
                              {
                                  "apartment": {
                                      "number": "202"}
                                  }
                              }, result.data)
