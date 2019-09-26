from django.test import TestCase
from condos.models import Apartment, Block
from graphene.test import Client
from alohomora.schema import schema


class ApartmentTestCase(TestCase):

    def setUp(self):
        Block.objects.create(number="1")
        block = Block.objects.get(number="1")
        Apartment.objects.create(number="101", block=block)

    def test_apartment_number(self):
        apartment = Apartment.objects.get(number="101")
        self.assertEqual(apartment.number, "101")

    def test_apartment_block(self):
        block = Block.objects.get(number="1")
        apartment = Apartment.objects.get(block=block)

        self.assertEqual(apartment.block.number, "1")

class BlockTestCase(TestCase):

    def setUp(self):
        Block.objects.create(number="1")

    def test_block_number(self):
        block = Block.objects.get(number="1")
        self.assertEqual(block.number, "1")

class GraphQLTestCase(TestCase):

    def setUp(self):
        self._client = Client(schema)
        block = Block.objects.create(number="1")
        Apartment.objects.create(number="101", block=block)

    def query(self, query: str):
        resp = self._client.execute(query)
        return resp

    def test_block_query(self):

        query = """
        {
            block(number:"1"){
                number
            }
        }
        """

        response = self.query(query=query)
        data = list(list(response['data'].items())[0][1].items())
        self.assertEqual(data[0][1], "1")

    def test_apartment_query(self):

        query = """
        {
            apartment(number:"101"){
                number
                block{
                    number
                }
            }
        }
        """

        response = self.query(query=query)
        data = list(list(response['data'].items())[0][1].items())

        self.assertEqual(list(data)[0][1], "101")
        self.assertEqual(list(data[1][1].items())[0][1], "1")
