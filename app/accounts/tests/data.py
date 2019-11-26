import json
from scipy.io.wavfile import read
from django.contrib.auth import get_user_model
from accounts.models import Visitor, Resident, Service, Entry, Admin, EntryVisitor
from condos.models import Apartment, Block
import accounts.utility as Utility

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
        )

def create_resident_test_account(resident_name):
    '''
    Create a resident accout for tests
    '''
    mfcc_resident = Utility.create_model_mfcc_from_wav_file(
        'accounts/tests/audios/' + resident_name + '_base.wav'
    )

    get_user_model().objects.create(
            email=resident_name + '@example.com',
            password=resident_name + '-password',
    )

    Resident.objects.create(
        complete_name=resident_name,
        email=resident_name + '@test.com',
        phone='99999999',
        cpf=resident_name,
        user=get_user_model().objects.get(email=resident_name + '@example.com'),
        mfcc_audio_speaking_phrase=mfcc_resident,
        mfcc_audio_speaking_name=mfcc_resident
    )

def initialize_voice_data():
    '''
    Create all resident accounts for tests
    '''
    create_resident_test_account('aline')
    # create_resident_test_account('baraky')
    # create_resident_test_account('felipe')
    # create_resident_test_account('luis')
    create_resident_test_account('marcos')
    # create_resident_test_account('mateus')
    # create_resident_test_account('paulo')
    # create_resident_test_account('pedro')
    # create_resident_test_account('rodrigo')
    create_resident_test_account('samuel')
    create_resident_test_account('sergio')
    create_resident_test_account('silva')
    create_resident_test_account('victor')
    create_resident_test_account('vitor')
