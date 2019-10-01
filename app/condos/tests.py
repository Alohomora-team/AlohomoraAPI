from django.test import TestCase
from condos.models import Apartment, Block
from graphene.test import Client
from alohomora.schema import schema
from graphql_jwt.testcases import JSONWebTokenTestCase



class GraphQLTestCase(JSONWebTokenTestCase, TestCase):

    def setUp(self):
        self._client = Client(schema)
        block = Block.objects.create(number="1")
        Apartment.objects.create(number="101", block=block)

    def query(self, query: str):
        resp = self._client.execute(query)
        return resp

    def test_block_mutation(self):

        mutation = '''
                        mutation{
                          createBlock(number: "1"){
                          number
                          }
                        }
        '''

        result = self.client.execute(mutation)
        self.assertIsNone(result.errors)
        self.assertDictEqual({"createBlock":
                              {
                                  "number": "1"}
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
