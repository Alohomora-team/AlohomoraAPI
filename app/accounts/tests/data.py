from condos.models import Apartment, Block
from accounts.models import Visitor, Resident, Service, Entry, Admin, EntryVisitor
from django.contrib.auth import get_user_model
import accounts.utility as Utility
import json

def initialize_data():
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
        apartment = Apartment.objects.create(number="101", block=block, id=5)
        Resident.objects.create(
            complete_name='resident-evil',
            password='resident-password',
            email='resident@example.com',
            cpf='12345678910',
            phone='42',
            mfcc_audio_speaking_phrase=[1.0, 2.0, 3.0, 4.0, 5.0],
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
        EntryVisitor.objects.create(
            id=5,
            visitor=Visitor.objects.get(cpf='29950509041'),
            apartment=apartment,
            date='2019-01-10',
            pending=True,
        )

def initialize_voice_data():
        mfcc_1 = Utility.create_model_mfcc(
            [x for x in range(32073)],
            samplerate=16000
        )
        mfcc_2 = Utility.create_model_mfcc(
            [3 * x for x in range(32073)],
            samplerate=16000
        )
        mfcc_3 = Utility.create_model_mfcc(
            [x**2  - 50 * x + 20 for x in range(32073)],
            samplerate=16000
        )
        mfcc_4 = Utility.create_model_mfcc(
            [x - 200 for x in range(32073)],
            samplerate=16000
        )
        mfcc_5 = Utility.create_model_mfcc(
            [x * 0.5 for x in range(32073)],
            samplerate=16000
        )

        get_user_model().objects.create(
            email='resident1@example.com',
            password='resident1-password',
        )
        get_user_model().objects.create(
            email='resident2@example.com',
            password='resident2-password',
        )
        get_user_model().objects.create(
            email='resident3@example.com',
            password='resident3-password',
        )
        get_user_model().objects.create(
            email='resident4@example.com',
            password='resident4-password',
        )
        get_user_model().objects.create(
            email='resident5@example.com',
            password='resident5-password',
        )

        Resident.objects.create(
            complete_name="Barry Allen",
            email="love_you_iris@starslab.com",
            phone="6133941598",
            user=get_user_model().objects.get(email='resident1@example.com'),
            cpf="0123456789",
            mfcc_audio_speaking_phrase=mfcc_1,
            mfcc_audio_speaking_name=mfcc_1,
        )

        Resident.objects.create(
            complete_name="Naruto Uzumaku",
            email="sereihokage@konoha.com",
            phone="6133941597",
            cpf="0123456781",
            user=get_user_model().objects.get(email='resident2@example.com'),
            mfcc_audio_speaking_phrase=mfcc_2,
            mfcc_audio_speaking_name=mfcc_2,
        )

        Resident.objects.create(
            complete_name="Max Steel",
            email="modoturbo@yahoo.com",
            phone="6133941596",
            cpf="0123456782",
            user=get_user_model().objects.get(email='resident3@example.com'),
            mfcc_audio_speaking_phrase=mfcc_3,
            mfcc_audio_speaking_name=mfcc_3,
        )

        Resident.objects.create(
            complete_name="Benjamin Tennyson",
            email="ben10@omnitrix.com",
            phone="33941595",
            cpf="0123456783",
            user=get_user_model().objects.get(email='resident4@example.com'),
            mfcc_audio_speaking_phrase=mfcc_4,
            mfcc_audio_speaking_name=mfcc_4,
        )

        Resident.objects.create(
            complete_name="Eren Jaeger",
            email="i_hate_marleyans@eldia.com",
            phone="99999999",
            cpf="0000000000",
            user=get_user_model().objects.get(email='resident5@example.com'),
            mfcc_audio_speaking_phrase=mfcc_5,
            mfcc_audio_speaking_name=mfcc_5,
        )
