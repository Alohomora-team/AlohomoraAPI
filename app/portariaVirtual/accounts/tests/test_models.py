from django.test import TestCase
from portariaVirtual.accounts.models import User
from portariaVirtual.accounts.models import Visitor

class UserModelTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        User.objects.create(
            complete_name='Big',
            email='Bob',
            password='12345',
            phone='12345',
            apartment='42',
            block='13'
        )

    def test_complete_name_label(self):
        user = User.objects.get(id=1)
        field_label = user._meta.get_field('complete_name').verbose_name
        self.assertEquals(field_label, 'complete name')

    def test_complete_name_max_length(self):
        user = User.objects.get(id=1)
        max_length = user._meta.get_field('complete_name').max_length
        self.assertEquals(max_length, 80)

    def test_email_label(self):
        user = User.objects.get(id=1)
        field_label = user._meta.get_field('email').verbose_name
        self.assertEquals(field_label, 'email')

    def test_email_max_length(self):
        user = User.objects.get(id=1)
        max_length = user._meta.get_field('email').max_length
        self.assertEquals(max_length, 90)

    def test_password_label(self):
        user = User.objects.get(id=1)
        field_label = user._meta.get_field('password').verbose_name
        self.assertEquals(field_label, 'password')

    def test_password_max_length(self):
        user = User.objects.get(id=1)
        max_length = user._meta.get_field('password').max_length
        self.assertEquals(max_length, 50)

    def test_phone_label(self):
        user = User.objects.get(id=1)
        field_label = user._meta.get_field('phone').verbose_name
        self.assertEquals(field_label, 'phone')

    def test_phone_max_length(self):
        user = User.objects.get(id=1)
        max_length = user._meta.get_field('phone').max_length
        self.assertEquals(max_length, 9)

    def test_apartment_label(self):
        user = User.objects.get(id=1)
        field_label = user._meta.get_field('apartment').verbose_name
        self.assertEquals(field_label, 'apartment')

    def test_block_label(self):
        user = User.objects.get(id=1)
        field_label = user._meta.get_field('block').verbose_name
        self.assertEquals(field_label, 'block')


class VisitorModelTest(TestCase):

    @classmethod
    def setUpTestData(cls):

        User.objects.create(
            complete_name='Big',
            email='Bob',
            password='12345',
            phone='12345',
            apartment='42',
            block='13'
        )

        Visitor.objects.create(
            owner=User.objects.get(id=1),
            complete_name='Big',
            email='Bob',
            phone='12345'
        )

    def test_complete_name_label(self):
        visitor = Visitor.objects.get(id=1)
        field_label = visitor._meta.get_field('complete_name').verbose_name
        self.assertEquals(field_label, 'complete name')

    def test_complete_name_max_length(self):
        visitor = Visitor.objects.get(id=1)
        max_length = visitor._meta.get_field('complete_name').max_length
        self.assertEquals(max_length, 80)

    def test_email_label(self):
        visitor = Visitor.objects.get(id=1)
        field_label = visitor._meta.get_field('email').verbose_name
        self.assertEquals(field_label, 'email')

    def test_email_max_length(self):
        visitor = Visitor.objects.get(id=1)
        max_length = visitor._meta.get_field('email').max_length
        self.assertEquals(max_length, 90)

    def test_phone_label(self):
        visitor = Visitor.objects.get(id=1)
        field_label = visitor._meta.get_field('phone').verbose_name
        self.assertEquals(field_label, 'phone')

    def test_phone_length(self):
        visitor = Visitor.objects.get(id=1)
        max_length = visitor._meta.get_field('phone').max_length
        self.assertEquals(max_length, 9)
