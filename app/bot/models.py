"""
Feedback django models
"""
from django.db import models

class Feedback(models.Model):
    """
    Save a comment from a user withou identified them
    """

    comment = models.TextField()

    def __str__(self):
        return self.comment
