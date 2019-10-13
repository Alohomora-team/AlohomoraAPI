import graphene
import graphql_jwt
import accounts.schema
import condos.schema
import feedbacks.schema


class Query(feedbacks.schema.Query, condos.schema.Query, accounts.schema.Query, graphene.ObjectType):
    pass


class Mutation(feedbacks.schema.Mutation, condos.schema.Mutation, accounts.schema.Mutation, graphene.ObjectType):
    token_auth = graphql_jwt.ObtainJSONWebToken.Field()
    verify_token = graphql_jwt.Verify.Field()
    refresh_token = graphql_jwt.Refresh.Field()

schema = graphene.Schema(query=Query, mutation=Mutation)
