# Generated by Django 2.2.5 on 2019-09-21 00:06

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('condos', '0006_auto_20190921_0005'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='apartment',
            name='owner',
        ),
        migrations.AddField(
            model_name='apartment',
            name='owner',
            field=models.ManyToManyField(null=True, to=settings.AUTH_USER_MODEL),
        ),
    ]
