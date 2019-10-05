# Generated by Django 2.2.5 on 2019-09-27 19:23

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('condos', '0010_auto_20190927_0123'),
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='password',
        ),
        migrations.AddField(
            model_name='user',
            name='admin',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='user',
            name='apartment',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='condos.Apartment'),
        ),
        migrations.AddField(
            model_name='user',
            name='block',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='condos.Block'),
        ),
        migrations.AddField(
            model_name='user',
            name='complete_name',
            field=models.CharField(default=django.utils.timezone.now, max_length=80),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='user',
            name='cpf',
            field=models.CharField(default=1, max_length=11),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='user',
            name='phone',
            field=models.CharField(default=1, max_length=15),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='user',
            name='voice_data',
            field=models.TextField(null=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='email',
            field=models.CharField(max_length=90, unique=True),
        ),
        migrations.CreateModel(
            name='Visitor',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('complete_name', models.CharField(max_length=80)),
                ('email', models.CharField(max_length=90)),
                ('phone', models.CharField(max_length=15)),
                ('cpf', models.CharField(max_length=11)),
                ('voice_data', models.TextField(null=True)),
                ('owner', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='accounts.User')),
            ],
        ),
    ]