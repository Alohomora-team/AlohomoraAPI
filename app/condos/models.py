from django.db import models

class Block(models.Model):
    number = models.CharField(max_length=4, primary_key=True)

    def __str__(self):
        return self.number

class Apartment(models.Model):
    class Meta:
        unique_together = ['number', 'block']

    number = models.CharField(max_length=6)

    block = models.ForeignKey(
        Block, related_name='apartments', on_delete=models.CASCADE)

    def __str__(self):
        return self.number
