"""
Tests of entry visitor
"""

import pytest
from graphql_jwt.testcases import JSONWebTokenTestCase
from django.test import TestCase
from graphene.test import Client
from alohomora.schema import schema
from django.contrib.auth import get_user_model
from accounts.models import Entry, Block, Apartment, EntryVisitor

@pytest.mark.usefixtures('test_data')
class EntryVisitorTest(JSONWebTokenTestCase, TestCase):
    """Test that information can be retrieved and created using graphql"""

    maxDiff = None
    def setUp(self):
        """SetUp for testing entry"""

        self._client = Client(schema)
        self.super_user = get_user_model().objects.create_superuser(email='admin@example',
                                                                    password='123')
        self.client.authenticate(self.super_user)

    def test_mutation_entry_visitor(self):
        """Test mutation createEntryVisitor"""

        mutation = '''
            mutation{
              createEntryVisitor(blockNumber: "1", apartmentNumber: "101", visitorCpf: "29950509041"){
            		entryVisitor{
                  visitor{
                  	cpf
                  }
                }
              }
            }
        '''
        result = self.client.execute(mutation)
        self.assertIsNone(result.errors)
        self.assertDictEqual({"createEntryVisitor": {
                                  "entryVisitor": {
                                    "visitor": {
                                      "cpf": "29950509041"
                                    },
                                  }
                                }
                              }, result.data)

    def test_query_all_entries_visitors(self):
        """Test query allEntriesVisitors"""

        mutation = '''
                    query {
                      allEntriesVisitors {
                        id
                        visitor{
                          completeName
                          cpf
                        }
                        apartment{
                          number
                        }
                      }
                    }
        '''
        result = self.client.execute(mutation)
        self.assertIsNone(result.errors)
        self.assertDictEqual({"allEntriesVisitors": [
                              {
                                "id": "5",
                                "visitor": {
                                  "completeName": "visitor",
                                  "cpf": "29950509041"
                                },
                                "apartment": {
                                  "number": "101"
                                }
                              }
                            ]
                          }, result.data)

    def test_query_entries_visitor(self):
        """Test mutation entriesVisitor"""

        mutation = '''
                    query {
                      entriesVisitor(cpf: "29950509041", blockNumber: "1", apartmentNumber: "101"){
                        visitor{
                          completeName
                          cpf
                        }
                    	}
                    }
        '''
        result = self.client.execute(mutation)
        self.assertIsNone(result.errors)
        self.assertDictEqual({"entriesVisitor": [
                              {
                                "visitor": {
                                  "completeName": "visitor",
                                  "cpf": "29950509041"
                                }
                              }
                            ]
                          }, result.data)

    def test_query_entries_visitor_filter(self):
        """Test mutation entriesVisitor"""

        mutation = '''
                    query {
                      entriesVisitor(blockNumber: "1", apartmentNumber: "101"){
                        visitor{
                          completeName
                          cpf
                        }
                    	}
                    }
        '''
        result = self.client.execute(mutation)
        self.assertIsNone(result.errors)
        self.assertDictEqual({"entriesVisitor": [
                              {
                                "visitor": {
                                  "completeName": "visitor",
                                  "cpf": "29950509041"
                                }
                              }
                            ]
                          }, result.data)
