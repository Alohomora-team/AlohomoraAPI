import graphene
from graphql_jwt.decorators import superuser_required
from accounts.models import Visitor
from accounts.types import VisitorType

class VisitorsQuery(graphene.AbstractType):
    """Used to read or fetch values"""

    all_visitors = graphene.List(VisitorType)


    visitor = graphene.Field(
        VisitorType,
        cpf=graphene.String()
        )

    # @superuser_required
    def resolve_all_visitors(self, info, **kwargs):
        """Query all visitors"""
        return Visitor.objects.all()

    # @superuser_required
    def resolve_visitor(self, info, **kwargs):
        """Query a specific visitor"""
        cpf = kwargs.get('cpf')

        return Visitor.objects.get(cpf=cpf)
