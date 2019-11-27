"""
Entries queries
"""

import graphene
from graphql_jwt.decorators import superuser_required
from condos.models import Apartment, Block
from accounts.models import Entry
from accounts.types import EntryType

class EntriesQuery(graphene.AbstractType):
    """Used to read or fetch values"""
    entries = graphene.List(EntryType)

    @superuser_required
    def resolve_entries(self, info, **kwargs):
        """Query all entries from residents"""
        return Entry.objects.all()
