import graphene

import accounts.schema

class Query(accounts.schema.Query, graphene.ObjectType):
    pass

schema = graphene.Schema(query=Query)
