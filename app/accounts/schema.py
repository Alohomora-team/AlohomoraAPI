from accounts.models import Visitor, Resident, Service, EntryVisitor, Entry, Admin
from condos.models import Apartment, Block
from condos.schema import ApartmentType, BlockType
from django.contrib.auth import get_user_model
from django.utils import timezone
from graphene_django import DjangoObjectType
from graphql_jwt.decorators import superuser_required, login_required
import accounts.utility as Utility
import datetime
import django.utils
import graphene
import secrets

class ResidentType(DjangoObjectType):
    """Resident as a object type"""
    class Meta:
        """Metadata"""
        model = Resident

class EntryType(DjangoObjectType):
    """Entry as a object type"""
    class Meta:
        """Metadata"""
        model = Entry

class ServiceType(DjangoObjectType):
    """Service as a object type"""
    class Meta:
        """Metadata"""
        model = Service

class VisitorType(DjangoObjectType):
    """Visitor as a object type"""
    class Meta:
        """Metadata"""
        model = Visitor

class EntryVisitorType(DjangoObjectType):
    """EntryVisitor as a object type"""
    class Meta:
        """Metadata"""
        model = EntryVisitor

class UserType(DjangoObjectType):
    """User as a object type"""
    class Meta:
        """Metadata"""
        model = get_user_model()

class AdminType(DjangoObjectType):
    """Admin as a object type"""
    class Meta:
        """Metadata"""
        model = Admin

class ServiceInput(graphene.InputObjectType):
    """Service input data types"""
    password = graphene.String()
    email = graphene.String()
    complete_name = graphene.String()

class ResidentInput(graphene.InputObjectType):
    """Resident input data types"""
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
    """Visitor input data types"""
    complete_name = graphene.String()
    cpf = graphene.String(required=True)
    new_cpf = graphene.String()


class CreateUser(graphene.Mutation):
    """Mutation from graphene for creating user"""
    user = graphene.Field(UserType)
    class Arguments:
        """Mutation arguments for create a user"""
        username = graphene.String(required=True)
        password = graphene.String(required=False)

    @login_required
    def mutate(self, info, password, username):
        """Method to execute the mutation"""
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
        """Mutation arguments for create a entry for a resident"""
        resident_cpf = graphene.String()
        apartment_number = graphene.String()

    def mutate(self, info, resident_cpf, apartment_number):
        """Method to execute the mutation"""
        resident = Resident.objects.filter(cpf=resident_cpf).first()
        apartment = Apartment.objects.filter(number=apartment_number).first()

        entry = Entry(resident=resident, apartment=apartment)
        entry.date = timezone.now()
        entry.save()

        return CreateEntry(resident=entry.resident, apartment=entry.apartment)



class CreateService(graphene.Mutation):
    """Mutation from graphene for creating service"""

    service = graphene.Field(ServiceType)

    class Arguments:
        """Mutation arguments for create a service"""
        password = graphene.String(required=True)
        email = graphene.String(required=True)
        complete_name = graphene.String(required=True)
    # @superuser_required
    def mutate(self, info, email, password, complete_name):
        """Method to execute the mutation"""
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
    """Mutation from graphene for creating resident"""

    resident = graphene.Field(ResidentType)

    class Arguments:
        """Mutation arguments for create a resident"""
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
        """Method to execute the mutation"""
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
        """Mutation arguments for create a visitor"""
        complete_name = graphene.String()
        cpf = graphene.String()

    # @superuser_required
    def mutate(self, info, **kwargs):
        """Method to execute the mutation"""
        complete_name = kwargs.get('complete_name')
        cpf = kwargs.get('cpf')

        visitor = Visitor(
            complete_name=complete_name,
            cpf=cpf
        )

        visitor.save()

        return CreateVisitor(visitor=visitor)

class CreateAdmin(graphene.Mutation):
    """Mutation from graphene for creating admin"""
    email = graphene.String()
    creator = graphene.Field(UserType)

    class Arguments:
        """Mutation arguments for create a admin"""
        email = graphene.String()
        password = graphene.String()

    # @superuser_required
    def mutate(self, info, email, password):
        """Method to execute the mutation"""
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
    """Mutation from graphene for creating entries from visitors"""

    entry_visitor = graphene.Field(EntryVisitorType)

    class Arguments:
        """Mutation arguments for create a entry for a visitor"""
        visitor_cpf = graphene.String()
        block_number = graphene.String()
        apartment_number = graphene.String()
        pending = graphene.Boolean()

    def mutate(self, info, **kwargs):
        """Method to execute the mutation"""
        visitor_cpf = kwargs.get('visitor_cpf')
        block_number = kwargs.get('block_number')
        apartment_number = kwargs.get('apartment_number')
        pending = kwargs.get('pending')

        visitor = Visitor.objects.get(cpf=visitor_cpf)

        if visitor is None:
            raise Exception('Visitor not found')

        block = Block.objects.get(number=block_number)

        if block is None:
            raise Exception('Block not found')

        apartment = Apartment.objects.get(
                block=block,
                number=apartment_number
                )

        if apartment is None:
            raise Exception('Apartment not found')

        entry = EntryVisitor(
                visitor=visitor,
                apartment=apartment,
                pending=pending
                )

        entry.save()

        return CreateEntryVisitor(entry_visitor=entry)

class DeleteResident(graphene.Mutation):
    """Mutation from graphene for deleting resident"""
    resident_email = graphene.String()

    class Arguments:
        """Mutation arguments for delete a resident"""
        resident_email = graphene.String(required=True)

    # @superuser_required
    def mutate(self, info, resident_email):
        """Method to execute the mutation"""
        resident = Resident.objects.get(email=resident_email)
        user = get_user_model().objects.get(email=resident_email)
        user.delete()
        resident.delete()

class DeleteService(graphene.Mutation):
    """Mutation from graphene for deleting service"""
    service_email = graphene.String()

    class Arguments:
        """Mutation arguments for delete aservice"""
        service_email = graphene.String(required=True)

    # @superuser_required
    def mutate(self, info, service_email):
        """Method to execute the mutation"""
        service = Service.objects.get(email=service_email)
        user = get_user_model().objects.get(email=service_email)
        user.delete()
        service.delete()

class DeleteVisitor(graphene.Mutation):
    """Mutation from graphene for deleting visitor"""
    cpf = graphene.String()

    class Arguments:
        """Mutation arguments for delete a visitor"""
        cpf = graphene.String(required=True)

    # @superuser_required
    def mutate(self, info, cpf):
        """Method to execute the mutation"""
        visitor = Visitor.objects.get(cpf=cpf)
        visitor.delete()

        return DeleteVisitor(
                cpf=cpf
                )

class DeleteEntryVisitorPending(graphene.Mutation):
    """Mutation from graphene for deleting visitor"""

    deleted = graphene.Boolean()

    class Arguments:
        """Mutation arguments for delete a visitor"""
        entry_id = graphene.String(required=True)

    def mutate(self, info, **kwargs):
        """Method to execute the mutation"""
        entry_id = kwargs.get('entry_id')

        entry_visitor = EntryVisitor.objects.get(id=entry_id)
        entry_visitor.delete()

        return DeleteEntryVisitorPending(deleted=True)

class DeleteEntriesVisitorsPending(graphene.Mutation):
    """Mutation from graphene for deleting visitor"""

    deleted = graphene.Boolean()

    class Arguments:
        """Mutation arguments for delete a visitor"""
        apartment_id = graphene.String(required=True)

    def mutate(self, info, **kwargs):
        """Method to execute the mutation"""
        apartment_id = kwargs.get('apartment_id')

        entry_visitors = EntryVisitor.objects.all().filter(apartment_id=apartment_id)
        entry_visitors.delete()

        return DeleteEntriesVisitorsPending(deleted=True)

class DeleteAdmin(graphene.Mutation):
    """Mutation from graphene for deleting admin"""
    email = graphene.String()

    class Arguments:
        """Mutation arguments for delete a admin"""
        email = graphene.String(required=True)

    # @superuser_required
    def mutate(self, info, email):
        """Method to execute the mutation"""
        user = info.context.user
        admin = get_user_model().objects.get(email=email)
        creator = Admin.objects.filter(admin=admin).first()

        if creator:
            creator = creator.creator

        if user != admin and user != creator:
            raise Exception('Logged in user is not related')

        admin.delete()

        return DeleteAdmin(
                email=email
                )

class UpdateService(graphene.Mutation):
    """Mutation from graphene for updating service"""
    user = graphene.Field(UserType)
    service = graphene.Field(ServiceType)

    class Arguments:
        """Mutation arguments for update a service"""
        service_data = ServiceInput()

    @login_required
    def mutate(self, info, service_data=None):
        """Method to execute the mutation"""
        user = info.context.user
        if user.is_service is not True:
            raise Exception('User is not service')
        email = user.email
        service = Service.objects.get(email=email)
        for key, value in service_data.items():
            if (key == 'password') and (value is not None):
                user.set_password(service_data.password)
            if (key == 'email') and (value is not None):
                setattr(user, key, value)
            if (key == 'email') and (value is not None):
                setattr(service, key, value)
            else:
                setattr(service, key, value)
        service.save()
        user.save()
        return UpdateService(user=user, service=service)

class UpdateResident(graphene.Mutation):
    """Mutation from graphene for updating resident"""
    user = graphene.Field(UserType)
    resident = graphene.Field(ResidentType)

    class Arguments:
        """Mutation arguments for update a resident"""
        resident_data = ResidentInput()

    @login_required
    def mutate(self, info, resident_data=None):
        """Method to execute the mutation"""
        user = info.context.user
        if user.is_resident is not True:
            raise Exception('User is not resident')
        email = user.email
        resident = Resident.objects.get(email=email)
        for key, value in resident_data.items():
            if (key == 'password') and (value is not None):
                user.set_password(resident_data.password)
            if (key == 'email') and (value is not None):
                setattr(user, key, value)
            if (key == 'email') and (value is not None):
                setattr(resident, key, value)
            else:
                setattr(resident, key, value)
        resident.save()
        user.save()
        return UpdateResident(user=user, resident=resident)

class UpdateVisitor(graphene.Mutation):
    """Mutation from graphene for updating visitor"""
    visitor = graphene.Field(VisitorType)

    class Arguments:
        """Mutation arguments for update a visitor"""
        complete_name = graphene.String()
        cpf = graphene.String(required=True)
        new_cpf = graphene.String()

    # @superuser_required
    def mutate(self, info, **kwargs):
        """Method to execute the mutation"""
        complete_name = kwargs.get('complete_name')
        cpf = kwargs.get('cpf')
        new_cpf = kwargs.get('new_cpf')

        visitor = Visitor.objects.get(cpf=cpf)

        if new_cpf:
            visitor.cpf = new_cpf

        if complete_name:
            visitor.complete_name = complete_name

        visitor.save()

        return UpdateVisitor(visitor=visitor)

# allow visitor entry
class UpdateEntryVisitorPending(graphene.Mutation):

    entry_id = graphene.String()
    entry_visitor_pending = graphene.Boolean()

    class Arguments:
        entry_id = graphene.String()

    def mutate(self, info, **kwargs):
        entry_id = kwargs.get('entry_id')

        entry = EntryVisitor.objects.get(id=entry_id)

        entry.pending = False

        entry.save()
        
        return UpdateEntryVisitorPending(
            entry_id=entry.id, 
            entry_visitor_pending=entry.pending
            )

class ActivateUser(graphene.Mutation):
    """Mutation from graphene for activating user"""
    user = graphene.Field(UserType)

    class Arguments:
        """Mutation arguments for activate a user"""
        user_email = graphene.String()
    def mutate(self, info, user_email):
        """Method to execute the mutation"""
        user = get_user_model().objects.get(email=user_email)
        user.is_active = True
        user.save()
        return ActivateUser(user=user)

class DeactivateUser(graphene.Mutation):
    """Mutation from graphene for deactivating user"""
    user = graphene.Field(UserType)

    class Arguments:
        """Mutation arguments for deactivate a user"""
        user_email = graphene.String()
    def mutate(self, info, user_email):
        """Method to execute the mutation"""
        user = get_user_model().objects.get(email=user_email)
        user.is_active = False
        user.save()
        return ActivateUser(user=user)

class Mutation(graphene.ObjectType):
    """Used to write or post values"""

    #create
    create_user = CreateUser.Field()
    create_resident = CreateResident.Field()
    create_entry = CreateEntry.Field()
    create_visitor = CreateVisitor.Field()
    create_entry_visitor = CreateEntryVisitor.Field()
    create_service = CreateService.Field()

    #update
    update_resident = UpdateResident.Field()
    update_visitor = UpdateVisitor.Field()
    update_entry_visitor_pending = UpdateEntryVisitorPending.Field()
    create_admin = CreateAdmin.Field()
    update_service = UpdateService.Field()
    activate_user = ActivateUser.Field()
    deactivate_user = DeactivateUser.Field()


    #delete
    delete_resident = DeleteResident.Field()
    delete_visitor = DeleteVisitor.Field()
    delete_entry_visitor_pending = DeleteEntryVisitorPending.Field()
    delete_entries_visitors_pending = DeleteEntriesVisitorsPending.Field()
    delete_service = DeleteService.Field()
    delete_admin = DeleteAdmin.Field()

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
        apartment_id=graphene.String(),
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

    # @superuser_required
    def resolve_all_visitors(self, info, **kwargs):
        """Query all visitors"""
        return Visitor.objects.all()

    # @superuser_required
    def resolve_residents(self, info, **kwargs):
        """Query all residents"""
        return Resident.objects.all()

    # @superuser_required
    def resolve_services(self, info, **kwargs):
        """Query all services"""
        return Service.objects.all()

    # @superuser_required
    def resolve_users(self, info, **kwargs):
        """Query all users"""
        return get_user_model().objects.all()

    # @superuser_required
    def resolve_all_admins(self, info, **kwargs):
        """Query all admins"""
        return Admin.objects.all()

    # @superuser_required
    def resolve_resident(self, info, **kwargs):
        """Query a specific resident"""
        email = kwargs.get('email')
        cpf = kwargs.get('cpf')

        if email is not None:
            return Resident.objects.get(email=email)

        if cpf is not None:
            return Resident.objects.get(cpf=cpf)

        return None

    # @superuser_required
    def resolve_visitor(self, info, **kwargs):
        """Query a specific visitor"""
        cpf = kwargs.get('cpf')

        return Visitor.objects.get(cpf=cpf)

    # @superuser_required
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
        apartment_id = kwargs.get('apartment_id')

        #Lista entradas pendentes de um apartamento de determinado bloco
        if apartment_id:

            return EntryVisitor.objects.filter(
                pending=True,
                apartment_id=apartment_id
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
