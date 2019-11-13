"""
Alohomora API routes
"""

from django.contrib import admin
from django.urls import path
from django.views.decorators.csrf import csrf_exempt
from graphene_django.views import GraphQLView
from rest_framework.authtoken.views import obtain_auth_token
from alohomora.schema import schema



urlpatterns = 
    path('admin/', admin.site.urls),
    path('graphql/', csrf_exempt(GraphQLView.as_view(schema=schema, graphiql=True))),
    path('api-token-auth/', obtain_auth_token, name='api_token_auth'),
]
