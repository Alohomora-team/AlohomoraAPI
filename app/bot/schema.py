import graphene

from graphene_django.types import DjangoObjectType

from bot.models import Feedback, UserData

class FeedbackType(DjangoObjectType):
    class Meta:
        model = Feedback

class UserDataType(DjangoObjectType):
    class Meta:
        model = UserData

class Query():
    all_feedbacks = graphene.List(FeedbackType)
    all_users_data = graphene.List(UserDataType)

    user_data = graphene.Field(
            UserDataType,
            chat_id=graphene.String(),
            cpf=graphene.String()
        )

    def resolve_all_feedbacks(self, info, **kwargs):
        return Feedback.objects.all()

    def resolve_all_users_data(self, info, **kwargs):
        return UserData.objects.all()

    def resolve_user_data(self, info, **kwargs):
        chat_id = kwargs.get('chat_id')
        cpf = kwargs.get('cpf')

        if chat_id and cpf:
            return UserData.objects.get(chat_id=chat_id, cpf=cpf)

        if chat_id:
            return UserData.objects.get(chat_id=chat_id)

        if cpf:
            return UserData.objects.get(cpf=cpf)

        return None

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

class CreateUserData(graphene.Mutation):
    chat_id = graphene.String()
    cpf = graphene.String()
    user_type = graphene.String()

    class Arguments:
        chat_id = graphene.String()
        cpf = graphene.String()
        user_type = graphene.String()

    def mutate(self, info, **kwargs):
        chat_id = kwargs.get('chat_id')
        cpf = kwargs.get('cpf')
        user_type = kwargs.get('user_type')

        user_data = UserData(
                chat_id=chat_id,
                cpf=cpf,
                user_type=user_type
            )
        
        user_data.save()

        return CreateUserData(
                chat_id=chat_id,
                cpf=cpf,
                user_type=user_data.get_user_type_display()
            ) 

class Mutation(graphene.ObjectType):
    create_feedback = CreateFeedback.Field()
    create_user_data = CreateUserData.Field()
