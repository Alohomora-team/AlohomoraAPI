from django.db import models

class Feedback(models.Model):

    comment = models.TextField()

    def __str__(self):
        return self.comment

class UserData(models.Model):

    USER_TYPES = (
            ('A', 'Admin'),
            ('R', 'Resident'),
            ('V', 'Visitor'),
        )

    chat_id = models.IntegerField(unique=True)
    cpf = models.CharField(max_length=11, unique=True)
    user_type = models.CharField(max_length=1, choices=USER_TYPES)

    def __str__(self):
        return self.chat_id
