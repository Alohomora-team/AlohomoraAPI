from django.test import TestCase
from condos.models import Apartment, Block


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
