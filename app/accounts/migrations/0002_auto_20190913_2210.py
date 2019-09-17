# Generated by Django 2.2.5 on 2019-09-13 22:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='apartment',
        ),
        migrations.RemoveField(
            model_name='user',
            name='block',
        ),
        migrations.AddField(
            model_name='user',
            name='admin',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='user',
            name='cpf',
            field=models.IntegerField(null=True),
        ),
        migrations.AddField(
            model_name='user',
            name='voice_data',
            field=models.TextField(null=True),
        ),
        migrations.AddField(
            model_name='visitor',
            name='cpf',
            field=models.IntegerField(null=True),
        ),
        migrations.AddField(
            model_name='visitor',
            name='voice_data',
            field=models.TextField(null=True),
        ),
    ]
