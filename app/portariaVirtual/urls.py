from django.contrib import admin
from django.urls import include, path

from graphene_django.views import GraphQLView
from portariaVirtual.schema import schema

from portariaVirtual.accounts import views

#rest framework imports
from rest_framework.authtoken.views import obtain_auth_token

urlpatterns = [
    path('admin/', admin.site.urls),
    path('graphql/', GraphQLView.as_view(schema=schema, graphiql=True)),
    path('hello/', views.HelloView.as_view(), name='hello'),
    path('api-token-auth/', obtain_auth_token, name='api_token_auth'),
]
