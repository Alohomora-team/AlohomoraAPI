import graphene

import portariaVirtual.accounts.schema

class Query(portariaVirtual.accounts.schema.Query, graphene.ObjectType):
    pass

schema = graphene.Schema(query=Query)
