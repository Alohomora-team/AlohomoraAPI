import graphene

from graphene_django.types import DjangoObjectType

from feedbacks.models import Feedback

class FeedbackType(DjangoObjectType):
    class Meta:
        model = Feedback

class Query():
    all_feedbacks = graphene.List(FeedbackType)

    feedback = graphene.Field(
        FeedbackType,
        number=graphene.String()
        )

    def resolve_feedback(self, info, **kwargs):
        number = kwargs.get('number')

        if number is not None:
            return Feedback.objects.get(number=number)

        return None

    def resolve_all_feedbacks(self, info, **kwargs):
        return Feedback.objects.all()


