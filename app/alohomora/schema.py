import graphene

import accounts.schema
import condos.schema

class Query(condos.schema.Query,
        accounts.schema.Query,
        graphene.ObjectType):
    pass

class Mutation(condos.schema.Mutation, graphene.ObjectType):
    pass

schema = graphene.Schema(query=Query, mutation=Mutation)
