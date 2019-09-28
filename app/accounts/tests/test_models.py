from django.test import TestCase
from accounts.models import User
from accounts.models import Visitor

class UserModelTest(TestCase):

    @classmethod
    def setUpTestData(cls):

        User.objects.create(
            complete_name='Big',
            email='Bob',
            password='12345',
            phone='12345',
        )

    def test_complete_name_label(self):
        user = User.objects.get(id=1)
        self.assertEquals(user.complete_name, 'Big')

    def test_complete_name_max_length(self):
        with self.assertRaises(Exception):
            User.objects.create(
                complete_name='a'*81,
                email='test@test.com',
                password='1234',
                phone='123412341234'
            )

    def test_email_label(self):
        user = User.objects.get(id=1)
        self.assertEquals(user.email, 'Bob')

    def test_email_max_length(self):

        with self.assertRaises(Exception):
            User.objects.create(
                complete_name='teste',
                email='1'*10,
                password='1234',
                phone='123412341234'
            )

    def test_phone_value(self):
        user = User.objects.get(id=1)
        self.assertEquals(user.phone, '12345')


class VisitorModelTest(TestCase):

    @classmethod
    def setUpTestData(cls):

        User.objects.create(
            complete_name='Big',
            email='Bob',
            password='12345',
            phone='12345',
        )

        Visitor.objects.create(
            owner=User.objects.get(complete_name='Big'),
            complete_name='Big',
            email='Bob',
            phone='12345'
        )

    def test_email_max_length(self):

        with self.assertRaises(Exception):
            Visitor.objects.create(
                owner=User.objects.get(complete_name='Big'),
                complete_name='Big',
                email='a'*100,
                phone='12345'
            )
