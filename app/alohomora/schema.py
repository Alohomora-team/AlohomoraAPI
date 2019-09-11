import graphene

import accounts.schema
import condos.schema

class Query(accounts.schema.Query, graphene.ObjectType):
    pass

class Query(condos.schema.Query, graphene.ObjectType):
    pass

schema = graphene.Schema(query=Query)
