import graphene

from graphene_django.types import DjangoObjectType

from bot.models import Feedback

class FeedbackType(DjangoObjectType):
    class Meta:
        model = Feedback

class Query():
    all_feedbacks = graphene.List(FeedbackType)

    feedback = graphene.Field(
        FeedbackType,
        comment=graphene.String()
        )

    def resolve_feedback(self, info, **kwargs):
        comment = kwargs.get('comment')

        if comment is not None:
            return Feedback.objects.get(comment=comment)

        return None

    def resolve_all_feedbacks(self, info, **kwargs):
        return Feedback.objects.all()


#Mutations

class CreateFeedback(graphene.Mutation):
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
    create_feedback = CreateFeedback.Field()


