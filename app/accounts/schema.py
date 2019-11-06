import graphene
from .mutations.entries import(
    CreateEntry,
    CreateEntryVisitor,
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
    delete_admin = DeleteAdmin.Field()

    update_service = UpdateService.Field()
    update_resident = UpdateResident.Field()
    update_visitor = UpdateVisitor.Field()

    activate_user = ActivateUser.Field()
    deactivate_user = DeactivateUser.Field()
