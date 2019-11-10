from condos.models import Apartment, Block
from accounts.models import Visitor, Resident, Service, Entry, Admin
from django.contrib.auth import get_user_model
import json

def initialize():
        get_user_model().objects.create(
            email='creator@example.com',
            password='creator-password',
            username='creator-username',
            is_active=True,
            is_admin=True,
            admin=True,
        )
        get_user_model().objects.create(
          email='admin2@example.com',
          password='admin2-password',
          is_active=True,
        )
        get_user_model().objects.create(
            email='service@example.com',
            password='service-password',
            username='service-username',
            is_active=True,
            is_service=True,
        )
        get_user_model().objects.create(
            email='resident@example.com',
            password='resident-password',
            username='resident-username',
            is_active=True,
            is_resident=True,
        )
        get_user_model().objects.create(
            email='desativado@example.com',
            password='desativado-password',
            username='desativado-username',
            is_active=False,
        )
        block = Block.objects.create(number="1")
        apartment = Apartment.objects.create(number="101", block=block)
        Resident.objects.create(
            complete_name='resident-evil',
            password='resident-password',
            email='resident@example.com',
            cpf='12345678910',
            phone='42',
            voice_data=json.dumps([x*10 for x in range(32000)]),
            admin=False,
            user=get_user_model().objects.get(email='resident@example.com'),
            apartment=apartment,
            block=block,
        )
        Visitor.objects.create(
            complete_name='visitor',
            cpf='29950509041',
        )
        Service.objects.create(
            complete_name='bob esponja',
            password='service-password',
            email='service@example.com',
            user=get_user_model().objects.get(email='service@example.com'),
        )
        Entry.objects.create(
            resident=Resident.objects.get(email='resident@example.com'),
            apartment=Apartment.objects.get(number='101')
        )
