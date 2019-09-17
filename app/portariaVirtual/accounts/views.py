from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse

# rest framework imports
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated 

class HelloView(APIView):

    #verify into header if token is valid
    permission_classes = (IsAuthenticated,) 

    def get(self, request):
        content = {'message': 'Hello, World!'}
        return Response(content)
