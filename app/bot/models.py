from django.db import models

class Feedback(models.Model):

    comment = models.TextField()

    def __str__(self):
        return self.comment