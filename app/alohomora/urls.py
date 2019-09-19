from django.contrib import admin
from django.urls import path
from graphene_django.views import GraphQLView
from alohomora.schema import schema
from rest_framework.authtoken.views import obtain_auth_token

urlpatterns = [
    path('admin/', admin.site.urls),
    path('graphql/', GraphQLView.as_view(schema=schema, graphiql=True)),
    path('api-token-auth/', obtain_auth_token, name='api_token_auth'),
]
