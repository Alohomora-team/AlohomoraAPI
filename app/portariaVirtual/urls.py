from django.contrib import admin
from django.urls import include, path

from graphene_django.views import GraphQLView
from portariaVirtual.schema import schema

from portariaVirtual.accounts import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('graphql/', GraphQLView.as_view(schema=schema, graphiql=True)),
    path('hello/', views.HelloView.as_view(), name='hello'),
]
