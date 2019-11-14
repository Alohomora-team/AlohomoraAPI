"""
Tests of entry
"""

import pytest
from graphql_jwt.testcases import JSONWebTokenTestCase
from django.test import TestCase
from graphene.test import Client
from alohomora.schema import schema
from django.contrib.auth import get_user_model
from accounts.models import Entry, Block, Apartment
from django.utils import timezone

@pytest.mark.usefixtures('test_data')
class ResidentTest(JSONWebTokenTestCase, TestCase):
    """Test that information can be retrieved and created using graphql"""
    maxDiff = None
    current_date_time = timezone.now()
    def setUp(self):
        self._client = Client(schema)
        self.super_user = get_user_model().objects.create_superuser(email='admin@example',
                                                                    password='123')
        self.client.authenticate(self.super_user)

    def test_query_entry(self):
        query = '''
            query{
              entries{
                resident{
                  cpf
                }
                apartment{
                  number
                }
            	}
            }
        '''
        result = self.client.execute(query)
        self.assertIsNone(result.errors)
        self.assertDictEqual({"entries": [
                              {
                                "resident": {
                                  "cpf": "12345678910"
                                },
                                "apartment": {
                                  "number": "101"
                                }
                              }
                            ]
                          }, result.data)

    def test_mutation_entry(self):
        block = Block.objects.get(number='1')
        apartment = Apartment.objects.create(number="202", block=block)
        mutation = '''
                mutation{
                  createEntry(apartmentNumber: "202", residentCpf: "12345678910"){
                	resident{
                    cpf
                  }
                }
                }
        '''
        result = self.client.execute(mutation)
        self.assertIsNone(result.errors)
        entry = Entry.objects.get(apartment=apartment)
        self.assertEqual(entry.date.hour, self.current_date_time.hour)
        self.assertEqual(entry.date.day, self.current_date_time.day)
        self.assertDictEqual({"createEntry":
                              {
                                  "resident": {
                                    "cpf": "12345678910"
                                  }
                                }
                              }, result.data)
