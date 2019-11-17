"""
Tests of condos
"""
import pytest
from graphene.test import Client
from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from condos.models import Apartment, Block
from alohomora.schema import schema
from graphql_jwt.testcases import JSONWebTokenTestCase

class GraphQLTestCase(JSONWebTokenTestCase, TestCase):
    """Test that information can be retrieved and created using graphql"""

    def setUp(self):
        """Setup data for testing condos"""

        self._client = Client(schema)
        block = Block.objects.create(number="1")
        Apartment.objects.create(number="101", block=block)
        self.super_user = get_user_model().objects.create_superuser(email='admin@exemplo',
                                                                    password='123')
        self.client.authenticate(self.super_user)

    def test_block_mutation(self):
        """Test mutation createBlock"""

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

    def test_all_blocks_query(self):
        """Test query allBlocks"""

        query = """
                query {
                  allBlocks {
                 	number
                  }
                }
        """

        result = self.client.execute(query)
        self.assertIsNone(result.errors)
        self.assertDictEqual({"allBlocks": [
                                  {
                                    "number": "1"
                                  }
                                ]
                              }, result.data)

    def test_block_query(self):
        """Test query block"""

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
        """Test mutation createApartment"""

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

    def test_all_apartments_query(self):
        """Test query allApartments"""

        query = """
        query {
          allApartments {
         	number
          }
        }
        """

        result = self.client.execute(query)
        self.assertIsNone(result.errors)
        self.assertDictEqual({"allApartments": [
                              {
                                "number": "101"
                              }
                            ]
                          }, result.data)

    def test_apartment_query(self):
        """Test query apartment"""

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
        """Test query aparments"""

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
        """Test mutation deleteApartment"""

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
        """Test mutation deleteBlock"""

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
        """Test mutation updateBlock"""

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
        """Test mutation updateApartment"""

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
