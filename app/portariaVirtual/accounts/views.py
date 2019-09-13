from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse

# rest framework imports
from rest_framework.views import APIView
from rest_framework.response import Response

class HelloView(APIView):
    def get(self, request):
        content = {'message': 'Hello, World!'}
        return Response(content)
