from django.test import TestCase
from django.contrib.auth import get_user_model
from accounts.models import Visitor, Service, Resident

class ResidentModelTest(TestCase):

    @classmethod
    def setUpTestData(cls):

        get_user_model().objects.create(
            email='exemplo@.com',
            password='12345',
            username='ok',
        )
        Resident.objects.create(
            complete_name='Big',
            email='Bob',
            phone='12345',
            user=get_user_model().objects.get(email='exemplo@.com')
        )

    def test_complete_name_label(self):
        resident = Resident.objects.get(user_id=1)
        self.assertEquals(resident.complete_name, 'Big')


    def test_complete_name_max_length(self):
        with self.assertRaises(Exception):
            Resident.objects.create(
                complete_name='a'*81,
                email='test@test.com',
                phone='123412341234'
            )

    def test_email_label(self):
        resident = Resident.objects.get(user_id=1)
        self.assertEquals(resident.email, 'Bob')

    def test_email_max_length(self):

        with self.assertRaises(Exception):
            Resident.objects.create(
                complete_name='teste',
                email='1'*100,
                phone='123412341234',
                user=get_user_model().objects.get(email='exemplo@.com'),

            )

    def test_phone_value(self):
        resident = Resident.objects.get(user_id=1)
        self.assertEquals(resident.phone, '12345')


class VisitorModelTest(TestCase):

    @classmethod
    def setUpTestData(cls):

        get_user_model().objects.create(
            email='exemplo@.com',
            password='12345',
            username='ok',
        )
        Resident.objects.create(
            complete_name='Big',
            email='Bob',
            phone='12345',
            user=get_user_model().objects.get(email='exemplo@.com'),
        )

        Visitor.objects.create(
            owner=Resident.objects.get(complete_name='Big'),
            complete_name='Big',
            email='Bob',
            phone='12345',
        )

    def test_email_max_length(self):

        with self.assertRaises(Exception):
            Visitor.objects.create(
                owner=Resident.objects.get(complete_name='Big'),
                complete_name='Big',
                email='a'*100,
                phone='12345'
            )


class ServiceModelTest(TestCase):

    @classmethod
    def setUpTestData(cls):

        get_user_model().objects.create(
            email='exemplo@.com',
            password='12345',
            username='ok',
        )

        Service.objects.create(
            email='squirtle@exemplo.com',
            complete_name='Eeeve',
            password='123',
            user=get_user_model().objects.get(email='exemplo@.com'),
        )

    def test_email_label(self):
        service = Service.objects.get(user_id=2)
        self.assertEquals(service.email, 'squirtle@exemplo.com')

    def test_email_max_length(self):

        with self.assertRaises(Exception):
            Service.objects.create(
                email='1'*100,
            )
