from django.db import models

class Block(models.Model):
    number = models.CharField(max_length=4)

    def save(self, *args, **kwargs):
        if Block.objects.filter(number=self.number).first() is not None:
            raise Exception('Object already exists')

        super(Block, self).save(*args, **kwargs)

    def __str__(self):
        return self.number

class Apartment(models.Model):
    number = models.CharField(max_length=6)

    block = models.ForeignKey(
        Block, related_name='apartments', on_delete=models.CASCADE)

    def save(self, *args, **kwargs):
        if Apartment.objects.filter(number=self.number, block=self.block).first() is not None:
            raise Exception('Object already exists')

        super(Apartment, self).save(*args, **kwargs)

    def __str__(self):
        return self.number
# Create your models here.
