import graphene
from condos.models import Apartment, Block
from django.contrib.auth import get_user_model
from graphql_jwt.decorators import superuser_required, login_required
from accounts.models import Visitor, Resident, Service, EntryVisitor, Entry, Admin
import accounts.utility as Utility
from accounts.types import (ResidentType,
                             ServiceType,
                             VisitorType,
                             UserType,
                             EntryType,
                             AdminType,
                             EntryVisitorType,)

class Query(graphene.AbstractType):
    """Used to read or fetch values"""

    me = graphene.Field(UserType)
    residents = graphene.List(ResidentType)
    all_visitors = graphene.List(VisitorType)
    services = graphene.List(ServiceType)
    users = graphene.List(UserType)
    all_entries_visitors = graphene.List(EntryVisitorType)
    entries = graphene.List(EntryType)
    unactives_users = graphene.List(UserType)
    all_admins = graphene.List(AdminType)

    voice_belongs_resident = graphene.Boolean(
        cpf=graphene.String(required=True),
        # TODO() - Remover um desses campos
        # talvez substituir voice_data por mfcc_data
        # A remoção é complicada pois existem dependencias
        voice_data=graphene.String(),
        mfcc_data=graphene.String()
    )

    resident = graphene.Field(
        ResidentType,
        email=graphene.String(),
        cpf=graphene.String()
        )

    visitor = graphene.Field(
        VisitorType,
        cpf=graphene.String()
        )

    admin = graphene.Field(
        graphene.List(AdminType),
        creator_email=graphene.String(),
        admin_email=graphene.String()
        )

    entries_visitor = graphene.Field(
        graphene.List(EntryVisitorType),
        cpf=graphene.String(),
        block_number=graphene.String(),
        apartment_number=graphene.String(),
        )
    entries_visitors_pending = graphene.Field(
        graphene.List(EntryVisitorType),
        block_number=graphene.String(),
        apartment_number=graphene.String(),
        )

    def resolve_unactives_users(self, info, **kwargs):
        """Query all unactives users"""
        return get_user_model().objects.filter(is_active=False)

    def resolve_all_entries_visitors(self, info, **kwargs):
        """Query all entries from visitors"""
        return EntryVisitor.objects.all()

    def resolve_entries(self, info, **kwargs):
        """Query all entries from residents"""
        return Entry.objects.all()

    @superuser_required
    def resolve_all_visitors(self, info, **kwargs):
        """Query all visitors"""
        return Visitor.objects.all()

    @superuser_required
    def resolve_residents(self, info, **kwargs):
        """Query all residents"""
        return Resident.objects.all()

    @superuser_required
    def resolve_services(self, info, **kwargs):
        """Query all services"""
        return Service.objects.all()

    @superuser_required
    def resolve_users(self, info, **kwargs):
        """Query all users"""
        return get_user_model().objects.all()

    @superuser_required
    def resolve_all_admins(self, info, **kwargs):
        """Query all admins"""
        return Admin.objects.all()

    @superuser_required
    def resolve_resident(self, info, **kwargs):
        """Query a specific resident"""
        email = kwargs.get('email')
        cpf = kwargs.get('cpf')

        if email is not None:
            return Resident.objects.get(email=email)

        if cpf is not None:
            return Resident.objects.get(cpf=cpf)

        return None

    @superuser_required
    def resolve_visitor(self, info, **kwargs):
        """Query a specific visitor"""
        cpf = kwargs.get('cpf')

        return Visitor.objects.get(cpf=cpf)

    @superuser_required
    def resolve_admin(self, info, **kwargs):
        """Query a specific admin"""
        creator_email = kwargs.get('creator_email')
        admin_email = kwargs.get('admin_email')

        admin = get_user_model().objects.filter(email=admin_email).first()
        creator = get_user_model().objects.filter(email=creator_email).first()

        if creator_email and admin_email:
            return Admin.objects.filter(
                    creator=creator,
                    admin=admin
                    )

        if creator_email:
            return Admin.objects.filter(
                    creator=creator
                    )

        if admin_email:
            return Admin.objects.filter(
                    admin=admin
                    )

    def resolve_entries_visitor(self, info, **kwargs):
        """Query all entries from a specific visitor"""
        cpf = kwargs.get('cpf')
        block_number = kwargs.get('block_number')
        apartment_number = kwargs.get('apartment_number')

        if cpf and block_number and apartment_number:
            visitor = Visitor.objects.get(cpf=cpf)
            block = Block.objects.get(number=block_number)
            apartment = Apartment.objects.get(
                    block=block,
                    number=apartment_number
                    )

            return EntryVisitor.objects.filter(
                    apartment=apartment,
                    visitor=visitor
                    )

        if block_number and apartment_number:
            block = Block.objects.get(number=block_number)
            apartment = Apartment.objects.get(
                    block=block,
                    number=apartment_number
                    )

            return EntryVisitor.objects.filter(apartment=apartment)

        if cpf:
            visitor = Visitor.objects.get(cpf=cpf)
            return EntryVisitor.objects.filter(visitor=visitor)


        return None

    def resolve_entries_visitors_pending(self, info, **kwargs):
        """Query all pending entries to a specific apartment"""
        block_number = kwargs.get('block_number')
        apartment_number = kwargs.get('apartment_number')

        #Lista entradas pendentes de um apartamento de determinado bloco
        if block_number and apartment_number:
            block = Block.objects.get(number=block_number)

            apartment = Apartment.objects.get(
                    block=block,
                    number=apartment_number
                    )

            return EntryVisitor.objects.filter(
                pending=True,
                apartment=apartment
                )

        return None

    def resolve_me(self, info):
        """Search for user features"""
        user = info.context.user
        if user.is_active is not True:
            raise Exception('User is NOT active')
        if user.is_service is True:
            raise Exception('User is service')
        if user.is_visitor is True:
            raise Exception('User is visitor')
        if user.is_resident is True:
            raise Exception('User is resident')
        return user

    def resolve_voice_belongs_resident(self, info, **kwargs):
        """Find out if the voice belongs to the resident"""
        resident_cpf = kwargs.get('cpf')
        voice_data = kwargs.get('voice_data')
        mfcc_data = kwargs.get('mfcc_data')

        if voice_data is not None:
            voice_sample = Utility.json_voice_data_to_mfcc(voice_data)
        else:
            voice_sample = Utility.json_to_numpy_array(mfcc_data)

        resident = Resident.objects.get(cpf=resident_cpf)
        others_residents = Resident.objects.exclude(cpf=resident_cpf)

        companion_residents = Query._retrieve_random_residents(others_residents, quantity=4)
        test_group = [resident] + companion_residents

        query_result = False
        if resident == Query._find_nearest_resident_by_voice(test_group, voice_sample):
            query_result = True

        return query_result

    @staticmethod
    def _retrieve_random_residents(residents, quantity):
        """Pick up random residents"""
        residents = residents[::1]
        if len(residents) <= quantity:
            return residents

        secure_random = secrets.SystemRandom()
        random_residents = secure_random.sample(residents, quantity)

        return random_residents

    @staticmethod
    def _find_nearest_resident_by_voice(residents, voice_sample):
        """Find the nearest resident by the voice"""
        nearest_resident = None
        lowest_dtw_score = 10**9

        for current_resident in residents:
            current_resident_voice_data = Utility.json_to_numpy_array(current_resident.voice_data)
            current_measure = Utility.compute_dtw_distance(voice_sample,
                                                           current_resident_voice_data)

            if current_measure < lowest_dtw_score:
                lowest_dtw_score = current_measure
                nearest_resident = current_resident

        return nearest_resident
