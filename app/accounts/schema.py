import graphene
from .mutations.entries import(
    CreateEntry,
)
from .mutations.entries_visitors import(
    CreateEntryVisitor,
    UpdateEntryVisitorPending,
    DeleteEntryVisitorPending,
    DeleteEntriesVisitorsPending,
)
from .mutations.residents import(
    CreateResident,
    DeleteResident,
    UpdateResident,
)
from .mutations.services import(
    CreateService,
    DeleteService,
    UpdateService,

)
from .mutations.users import(
    CreateUser,
    ActivateUser,
    DeactivateUser,
)
from .mutations.visitors import(
    CreateVisitor,
    DeleteVisitor,
    UpdateVisitor,
)
from .mutations.admins import(
    CreateAdmin,
    DeleteAdmin,
)
class Mutation(graphene.ObjectType):
    """Used to write or post values"""

    #create
    create_user = CreateUser.Field()
    create_resident = CreateResident.Field()
    create_entry = CreateEntry.Field()
    create_visitor = CreateVisitor.Field()
    create_entry_visitor = CreateEntryVisitor.Field()
    create_admin = CreateAdmin.Field()
    create_service = CreateService.Field()

    #update
    update_resident = UpdateResident.Field()
    update_visitor = UpdateVisitor.Field()
    update_entry_visitor_pending = UpdateEntryVisitorPending.Field()
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