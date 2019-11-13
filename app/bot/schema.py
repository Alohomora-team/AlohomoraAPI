"""
Binding graphene types and Creating Queries and Mutation from the module
"""

import graphene

from graphene_django.types import DjangoObjectType
from bot.models import Feedback

class FeedbackType(DjangoObjectType):
	"""
	Binding feedback django models in 
	graphene type
	"""
    class Meta:
        model = Feedback

class Query():
	"""
	Retrieve all feedbacks from database
	"""
    all_feedbacks = graphene.List(FeedbackType)

    def resolve_all_feedbacks(self, info, **kwargs):
        return Feedback.objects.all()

#Mutations

class CreateFeedback(graphene.Mutation):
	"""
	Create a feedback
	"""
    comment = graphene.String()

    class Arguments:
        comment = graphene.String()

    def mutate(self, info, comment):
        feedback = Feedback(comment=comment)
        feedback.save()

        return CreateFeedback(
            comment=feedback.comment
            )

class Mutation(graphene.ObjectType):
	"""
	Binding Mutation
	"""
    create_feedback = CreateFeedback.Field()
