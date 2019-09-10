from django.contrib import admin
from django.urls import include, path

from graphene_django.views import GraphQLView
from alohomora.schema import schema

urlpatterns = [
    path('admin/', admin.site.urls),
    path('graphql/', GraphQLView.as_view(schema=schema, graphiql=True)),
]
