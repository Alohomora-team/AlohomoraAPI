from graphene.test import Client
from django.test import TestCase
from bot.models import Feedback
from alohomora.schema import schema

# Create your tests here.

class GraphQLTestCase(TestCase):

    def setUp(self):
        self._client = Client(schema)
        Feedback.objects.create(comment="Test")

    def query(self, query: str):
        response = self._client.execute(query)
        return response

    def test_feedback_query(self):
        query = """
        {
            allFeedbacks{
                comment
            }
        }
        """

        result = self._client.execute(query)
        self.assertDictEqual(
            {"allFeedbacks": [
                {
                    "comment": "Test"
                }
                ]
            }, result["data"])

    def test_feedback_mutation(self):
        mutation = """
        mutation{
            createFeedback(comment: "Test2"){
                comment
            }
        }
        """

        result = self._client.execute(mutation)
        self.assertDictEqual(
            {"createFeedback":
                    {
                        "comment": "Test2"
                    }
            }, result["data"])
