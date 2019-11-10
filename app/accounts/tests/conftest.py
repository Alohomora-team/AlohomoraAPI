import pytest
from .data import initialize
from alohomora.schema import schema
from graphene.test import Client
from django.test import TestCase
from graphql_jwt.testcases import JSONWebTokenTestCase

@pytest.fixture(scope="class")
def test_data():
    return initialize()
