import secrets
import graphene
from graphene_django import DjangoObjectType
from accounts.models import Visitor, Resident, Service, EntryVisitor
import accounts.utility as Utility
from condos.models import Apartment, Block
from condos.schema import ApartmentType
from django.contrib.auth import get_user_model
from graphql_jwt.decorators import superuser_required
from graphql_jwt.decorators import login_required
from accounts.models import Visitor, Resident, Service, Entry, Admin
import accounts.utility as Utility
from condos.models import Apartment, Block
from condos.schema import ApartmentType, BlockType
from django.contrib.auth import get_user_model
from graphql_jwt.decorators import superuser_required, login_required
from django.utils import timezone
import datetime
import django.utils

class ResidentType(DjangoObjectType):
    class Meta:
        model = Resident

class EntryType(DjangoObjectType):
    class Meta:
        model = Entry

class ServiceType(DjangoObjectType):
    class Meta:
        model = Service

class VisitorType(DjangoObjectType):
    class Meta:
        model = Visitor

class EntryVisitorType(DjangoObjectType):
    class Meta:
        model = EntryVisitor

class UserType(DjangoObjectType):
    class Meta:
        model = get_user_model()

class AdminType(DjangoObjectType):
    class Meta:
        model = Admin

class ServiceInput(graphene.InputObjectType):
    password = graphene.String()
    email = graphene.String()
    complete_name = graphene.String()

class ResidentInput(graphene.InputObjectType):
    complete_name = graphene.String()
    email = graphene.String()
    phone = graphene.String()
    cpf = graphene.String()
    apartment = graphene.String()
    block = graphene.String()
    password = graphene.String()
    voice_data = graphene.String()
    mfcc_data = graphene.String()

class VisitorInput(graphene.InputObjectType):
    complete_name = graphene.String()
    email = graphene.String()
    phone = graphene.String()
    cpf = graphene.String()
    voice_data = graphene.String()
    owner_cpf = graphene.String()


class CreateUser(graphene.Mutation):
    """Mutation from graphene for creating service"""
    user = graphene.Field(UserType)
    class Arguments:
        username = graphene.String(required=True)
        password = graphene.String(required=False)
    @login_required
    def mutate(self, info, password, username):
        user = get_user_model()(
            username=username,
            password=password,
        )
        user.set_password(password)
        user.save()

        return CreateUser(user=user)

class CreateEntry(graphene.Mutation):
    """Mutation from graphene for creating entry"""

    resident = graphene.Field(ResidentType)
    apartment = graphene.Field(ApartmentType)

    resident_cpf = graphene.String()
    apartment_number = graphene.String()

    class Arguments:
        resident_cpf = graphene.String()
        apartment_number = graphene.String()

    def mutate(self, info, resident_cpf, apartment_number):
        resident = Resident.objects.filter(cpf=resident_cpf).first()
        apartment = Apartment.objects.filter(number=apartment_number).first()

        entry = Entry(resident=resident, apartment=apartment)
        entry.date = timezone.now()
        entry.save()

        return CreateEntry(resident = entry.resident, apartment = entry.apartment)



class CreateService(graphene.Mutation):
    """Mutation from graphene for creating service"""

    service = graphene.Field(ServiceType)

    class Arguments:
        password = graphene.String(required=True)
        email = graphene.String(required=True)
        complete_name = graphene.String(required=True)
    @superuser_required
    def mutate(self, info, email, password, complete_name):
        user = get_user_model()(email=email)
        user.set_password(password)
        user.is_service = True
        user.save()
        service = Service.objects.create(user=user)
        service = Service(
            complete_name=complete_name,
            email=email,
            user=user,
        )
        service.save()

        return CreateService(service=service)

class CreateResident(graphene.Mutation):
    """Mutation from graphene for creating user"""

    resident = graphene.Field(ResidentType)

    class Arguments:
        complete_name = graphene.String(required=True)
        email = graphene.String(required=True)
        phone = graphene.String(required=True)
        cpf = graphene.String(required=True)
        apartment = graphene.String(required=True)
        block = graphene.String(required=True)
        password = graphene.String(required=False)

        # TODO() - Remover um desses campos
        # talvez substituir voice_data por mfcc_data
        # A remoção é complicada pois existem dependencias
        voice_data = graphene.String()
        mfcc_data = graphene.String()

        mfcc_audio_speaking_name = graphene.String()
    def mutate(self, info, **kwargs):
        voice_data = kwargs.get('voice_data')
        mfcc_data = kwargs.get('mfcc_data')
        cpf = kwargs.get('cpf')
        complete_name = kwargs.get('complete_name')
        phone = kwargs.get('phone')
        email = kwargs.get('email')
        apartment = kwargs.get('apartment')
        block = kwargs.get('block')
        password = kwargs.get('password')
        mfcc_audio_speaking_name = kwargs.get('mfcc_audio_speaking_name')

        user = get_user_model()(email=email)
        user.set_password(password)
        user.is_resident = True

        block_obj = Block.objects.filter(number=block).first()

        if voice_data is not None:
            try:
                voice_data = Utility.json_voice_data_to_json_mfcc(voice_data)
            except:
                raise Exception('Invalid voice data')
        else:
            voice_data = mfcc_data

        if block_obj is None:
            raise Exception('Block not found')


        if Apartment.objects.filter(number=apartment, block=block_obj).first() is None:
            raise Exception('Apartment not found')

        user.save()
        resident = Resident.objects.create(user=user)
        resident = Resident(
            complete_name=complete_name,
            email=email,
            phone=phone,
            cpf=cpf,
            voice_data=voice_data,
            user=user,
            apartment=Apartment.objects.get(number=apartment, block=block_obj),
            mfcc_audio_speaking_name=mfcc_audio_speaking_name
        )
        resident.save()
        return CreateResident(resident=resident)

class CreateVisitor(graphene.Mutation):
    """Mutation from graphene for creating visitor"""
    visitor = graphene.Field(VisitorType)

    class Arguments:
        complete_name = graphene.String()
        email = graphene.String()
        phone = graphene.String()
        cpf = graphene.String()
        voice_data = graphene.String()
        owner_cpf = graphene.String()

    @login_required
    def mutate(self, info, **kwargs):
        voice_data = kwargs.get('voice_data')
        cpf = kwargs.get('cpf')
        complete_name = kwargs.get('complete_name')
        phone = kwargs.get('phone')
        email = kwargs.get('email')
        owner_cpf = kwargs.get('owner_cpf')

        resident = Resident.objects.filter(cpf=owner_cpf).first()

        if voice_data is not None:
            voice_data = Utility.json_voice_data_to_json_mfcc(voice_data)

        visitor = Visitor(
            complete_name=complete_name,
            email=email,
            cpf=cpf,
            phone=phone,
            voice_data=voice_data,
            owner=resident,
        )
        if resident is None:
            raise Exception('Resident not found')

        visitor.save()

        return CreateVisitor(visitor=visitor)

class CreateAdmin(graphene.Mutation):
    email = graphene.String()
    creator = graphene.Field(UserType)

    class Arguments:
        email = graphene.String()
        password = graphene.String()

    @superuser_required
    def mutate(self, info, email, password):
        admin = get_user_model().objects.create_superuser(
            email=email,
            password=password,
        )

        admin.set_password(password)
        admin.save()

        creator = info.context.user

        management = Admin(
                admin=admin,
                creator=creator
                )

        management.save()

        return CreateAdmin(
            email=email,
            creator=creator
            )


class CreateEntryVisitor(graphene.Mutation):
    """Mutation from graphene for creating entry"""

    visitor = graphene.Field(VisitorType)
    apartment = graphene.Field(ApartmentType)

    visitor_cpf = graphene.String()
    block_number = graphene.String()
    apartment_number = graphene.String()
    pending = graphene.Boolean()

    class Arguments:
        visitor_cpf = graphene.String()
        block_number = graphene.String()
        apartment_number = graphene.String()
        pending = graphene.Boolean()

    def mutate(self, info, visitor_cpf, block_number, apartment_number, pending):
        visitor = Visitor.objects.filter(cpf=visitor_cpf).first()

        if visitor is None:
            raise Exception('Visitor not found')

        block = Block.objects.filter(number=block_number).first()

        if block is None:
            raise Exception('Block not found')

        apartment = Apartment.objects.filter(block=block, number=apartment_number).first()

        if apartment is None:
            raise Exception('Apartment not found')

        entry = EntryVisitor(visitor=visitor, apartment=apartment, pending=pending)
        entry.save()

        return CreateEntryVisitor(
            visitor_cpf=entry.visitor.cpf,
            block_number=entry.apartment.block,
            apartment_number=entry.apartment,
            pending=pending
            )
class DeleteResident(graphene.Mutation):
    resident_email = graphene.String()

    class Arguments:
        resident_email = graphene.String(required=True)

    @superuser_required
    def mutate(self, info, resident_email):
        resident = Resident.objects.get(email=resident_email)
        user = get_user_model().objects.get(email=resident_email)
        user.delete()
        resident.delete()

class DeleteService(graphene.Mutation):
    service_email = graphene.String()

    class Arguments:
        service_email = graphene.String(required=True)

    @superuser_required
    def mutate(self, info, service_email):
        service = Service.objects.get(email=service_email)
        user = get_user_model().objects.get(email=service_email)
        user.delete()
        service.delete()

class DeleteVisitor(graphene.Mutation):
    visitor_email = graphene.String()

    class Arguments:
        visitor_email = graphene.String(required=True)

    def mutate(self, info, visitor_email):
        visitor = Visitor.objects.get(email=visitor_email)
        visitor.delete()

class UpdateService(graphene.Mutation):
    user = graphene.Field(UserType)
    service = graphene.Field(ServiceType)

    class Arguments:
        service_data = ServiceInput()

    @login_required
    def mutate(self, info, service_data=None):
        user = info.context.user
        if user.is_service is not True:
            raise Exception('User is not service')
        email = user.email
        service = Service.objects.get(email=email)
        for k, v in service_data.items():
            if (k == 'password') and (v is not None):
                user.set_password(service_data.password)
            if (k == 'email') and (v is not None):
                setattr(user, k, v)
            if (k == 'email') and (v is not None):
                setattr(service, k, v)
            else:
                setattr(service, k, v)
        service.save()
        user.save()
        return UpdateService(user=user, service=service)

class UpdateResident(graphene.Mutation):
    user = graphene.Field(UserType)
    resident = graphene.Field(ResidentType)

    class Arguments:
        resident_data = ResidentInput()

    @login_required
    def mutate(self, info, resident_data=None):
        user = info.context.user
        if user.is_resident is not True:
            raise Exception('User is not resident')
        email = user.email
        resident = Resident.objects.get(email=email)
        for k, v in resident_data.items():
            if (k == 'password') and (v is not None):
                user.set_password(resident_data.password)
            if (k == 'email') and (v is not None):
                setattr(user, k, v)
            if (k == 'email') and (v is not None):
                setattr(resident, k, v)
            else:
                setattr(resident, k, v)
        resident.save()
        user.save()
        return UpdateResident(user=user, resident=resident)

class UpdateVisitor(graphene.Mutation):
    visitor = graphene.Field(VisitorType)
    user = graphene.Field(UserType)

    class Arguments:
        visitor_data = VisitorInput()

    @login_required
    def mutate(self, info, visitor_data=None):
        user = info.context.user
        if user.is_resident is not True:
            raise Exception('User is not resident')
        email = user.email
        resident = Resident.objects.get(email=email)
        visitor = Visitor.objects.get(owner=resident)

        for k, v in visitor_data.items():
            setattr(visitor, k, v)

        visitor.save()
        return UpdateVisitor(user=user, visitor=visitor)
class ActivateUser(graphene.Mutation):
    """Mutation from graphene for activating user"""
    user = graphene.Field(UserType)

    class Arguments:
        user_email = graphene.String()
    def mutate(self, info, user_email):
        user = get_user_model().objects.get(email=user_email)
        user.is_active = True
        user.save()
        return ActivateUser(user=user)

class DeactivateUser(graphene.Mutation):
    """Mutation from graphene for activating user"""
    user = graphene.Field(UserType)

    class Arguments:
        user_email = graphene.String()
    def mutate(self, info, user_email):
        user = get_user_model().objects.get(email=user_email)
        user.is_active = False
        user.save()
        return ActivateUser(user=user)

class Mutation(graphene.ObjectType):
    """Used to write or post values"""

    create_user = CreateUser.Field()
    create_visitor = CreateVisitor.Field()
    create_entry = CreateEntry.Field()
    create_service = CreateService.Field()
    create_resident = CreateResident.Field()
    create_entry_visitor = CreateEntryVisitor.Field()
    create_admin = CreateAdmin.Field()

    delete_resident = DeleteResident.Field()
    delete_service = DeleteService.Field()
    delete_visitor = DeleteVisitor.Field()
    update_service = UpdateService.Field()
    update_resident = UpdateResident.Field()
    update_visitor = UpdateVisitor.Field()
    activate_user = ActivateUser.Field()
    deactivate_user = DeactivateUser.Field()

class Query(graphene.AbstractType):
    """Used to read or fetch values"""

    me = graphene.Field(UserType)
    residents = graphene.List(ResidentType)
    visitors = graphene.List(VisitorType)
    services = graphene.List(ServiceType)
    users = graphene.List(UserType)
    entries_visitors = graphene.List(EntryVisitorType, cpf=graphene.String())
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
        email=graphene.String(),
        cpf=graphene.String()
        )

    admin = graphene.Field(
        graphene.List(AdminType),
        creator_email=graphene.String(),
        admin_email=graphene.String()
        )

    def resolve_unactives_users(self, info, **kwargs):
        return get_user_model().objects.filter(is_active=False)

    entries_visitors_filtered = graphene.Field(
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

    def resolve_entries_visitors(self, info, **kwargs):
        return EntryVisitor.objects.all()
    def resolve_entries(self, info, **kwargs):
        return Entry.objects.all()
    @superuser_required
    def resolve_visitors(self, info, **kwargs):
        return Visitor.objects.all()
    @superuser_required
    def resolve_residents(self, info, **kwargs):
        return Resident.objects.all()
    @superuser_required
    def resolve_services(self, info, **kwargs):
        return Service.objects.all()
    @superuser_required
    def resolve_users(self, info, **kwargs):
        return get_user_model().objects.all()
    @superuser_required
    def resolve_all_admins(self, info, **kwargs):
        return Admin.objects.all()

    @superuser_required
    def resolve_resident(self, info, **kwargs):
        email = kwargs.get('email')
        cpf = kwargs.get('cpf')

        if email is not None:
            return Resident.objects.get(email=email)

        if cpf is not None:
            return Resident.objects.get(cpf=cpf)

        return None
    @superuser_required
    def resolve_visitor(self, info, **kwargs):
        email = kwargs.get('email')
        cpf = kwargs.get('cpf')

        if email is not None:
            return Visitor.objects.get(email=email)

        if cpf is not None:
            return Visitor.objects.get(cpf=cpf)

        return None

    @superuser_required
    def resolve_admin(self, info, **kwargs):
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

    def resolve_entries_visitors_filtered(self, info, **kwargs):
        cpf = kwargs.get('cpf')
        block_number = kwargs.get('block_number')
        apartment_number = kwargs.get('apartment_number')

        if cpf is not None:
            visitor = Visitor.objects.get(cpf=cpf)
            return EntryVisitor.objects.filter(visitor=visitor)

        if block_number and apartment_number is not None:
            block = Block.objects.get(number=block_number)
            apartment = Apartment.objects.get(block=block, number=apartment_number)
            return EntryVisitor.objects.filter(apartment=apartment)

        return None
    def resolve_entries_visitors_pending(self, info, **kwargs):
        block_number = kwargs.get('block_number')
        apartment_number = kwargs.get('apartment_number')

        #Lista entradas pendentes de um apartamento de determinado bloco
        if block_number and apartment_number is not None:
            block = Block.objects.get(number=block_number)
            apartment = Apartment.objects.get(block=block, number=apartment_number)
            return EntryVisitor.objects.filter(
                pending=True,
                apartment=apartment
                )
        return None
    def resolve_me(self, info):
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
        residents = residents[::1]
        if len(residents) <= quantity:
            return residents

        secure_random = secrets.SystemRandom()
        random_residents = secure_random.sample(residents, quantity)

        return random_residents

    @staticmethod
    def _find_nearest_resident_by_voice(residents, voice_sample):
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
