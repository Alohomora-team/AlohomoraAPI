"""
Binding all queries and mutations
"""

import graphene
import graphql_jwt
import accounts.schema
import accounts.queries.residents
import accounts.queries.users
import accounts.queries.admins
import accounts.queries.visitors
import accounts.queries.entries
import accounts.queries.entries_visitors
import accounts.queries.services
import condos.schema
import condos.queries
import bot.schema

class Query(
        bot.schema.Query,
        condos.queries.Query,
        accounts.queries.admins.AdminsQuery,
        accounts.queries.entries.EntriesQuery,
        accounts.queries.entries_visitors.EntriesVisitorsQuery,
        accounts.queries.residents.ResidentsQuery,
        accounts.queries.services.ServicesQuery,
        accounts.queries.users.UsersQuery,
        accounts.queries.visitors.VisitorsQuery,
        graphene.ObjectType,
        ):
	"""
	Just inherit from queries classes and binds in main schema
	"""
    pass


class Mutation(
        bot.schema.Mutation,
        condos.schema.Mutation,
        accounts.schema.Mutation,
        graphene.ObjectType
        ):
	"""
	Inherit from mutations and binds them in main schema
	"""

    token_auth = graphql_jwt.ObtainJSONWebToken.Field()
    verify_token = graphql_jwt.Verify.Field()
    refresh_token = graphql_jwt.Refresh.Field()

schema = graphene.Schema(query=Query, mutation=Mutation)
