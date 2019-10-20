# Generated by Django 2.2.5 on 2019-10-20 21:57

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0011_update_proxy_permissions'),
        ('condos', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('first_name', models.CharField(blank=True, max_length=30, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('is_resident', models.BooleanField(default=False, verbose_name='student status')),
                ('is_service', models.BooleanField(default=False, verbose_name='service status')),
                ('is_visitor', models.BooleanField(default=False, verbose_name='visitor status')),
                ('username', models.CharField(max_length=40, null=True)),
                ('email', models.CharField(max_length=40, unique=True)),
                ('password', models.CharField(max_length=80)),
                ('is_admin', models.BooleanField(default=False)),
                ('admin', models.BooleanField(default=False)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Resident',
            fields=[
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
                ('complete_name', models.CharField(max_length=80)),
                ('email', models.CharField(max_length=90, unique=True)),
                ('phone', models.CharField(max_length=15)),
                ('cpf', models.CharField(max_length=11)),
                ('admin', models.BooleanField(default=False)),
                ('password', models.CharField(max_length=80)),
                ('voice_data', models.TextField(null=True)),
                ('mfcc_audio_speaking_name', models.TextField(null=True)),
                ('apartment', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='condos.Apartment')),
                ('block', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='condos.Block')),
            ],
        ),
        migrations.CreateModel(
            name='Service',
            fields=[
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
                ('complete_name', models.CharField(max_length=80)),
                ('email', models.CharField(max_length=90)),
                ('password', models.CharField(max_length=80)),
            ],
        ),
        migrations.CreateModel(
            name='Entry',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateTimeField(auto_now=True)),
                ('apartment', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='condos.Apartment')),
            ],
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
                ('owner', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='accounts.Resident')),
            ],
        ),
        migrations.AddField(
            model_name='resident',
            name='entries',
            field=models.ManyToManyField(related_name='entries', through='accounts.Entry', to='condos.Apartment'),
        ),
        migrations.AddField(
            model_name='entry',
            name='resident',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='accounts.Resident'),
        ),
    ]
