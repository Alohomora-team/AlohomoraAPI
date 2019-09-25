# Generated by Django 2.2.5 on 2019-09-21 00:05

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('condos', '0005_auto_20190920_2357'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='apartment',
            name='owner',
        ),
        migrations.AddField(
            model_name='apartment',
            name='owner',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]