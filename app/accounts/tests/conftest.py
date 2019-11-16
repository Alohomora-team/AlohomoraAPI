import pytest
from .data import initialize_data, initialize_voice_data
from alohomora.schema import schema
from graphene.test import Client
from django.test import TestCase
from graphql_jwt.testcases import JSONWebTokenTestCase

@pytest.fixture(scope="class")
def test_data():
    return initialize_data()

@pytest.fixture(scope="class")
def test_voice_data():
    return initialize_voice_data()
