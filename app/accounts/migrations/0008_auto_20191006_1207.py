# Generated by Django 2.2.5 on 2019-10-06 12:07

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('condos', '0010_auto_20190927_0123'),
        ('auth', '0011_update_proxy_permissions'),
        ('accounts', '0007_auto_20191001_0057'),
    ]

    operations = [
        migrations.CreateModel(
            name='Resident',
            fields=[
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
                ('complete_name', models.CharField(max_length=80)),
                ('email', models.CharField(max_length=90, unique=True)),
                ('phone', models.CharField(max_length=15)),
                ('cpf', models.CharField(max_length=11)),
                ('admin', models.BooleanField(default=False)),
                ('voice_data', models.TextField(null=True)),
                ('apartment', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='condos.Apartment')),
                ('block', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='condos.Block')),
            ],
        ),
        migrations.AlterModelOptions(
            name='service',
            options={},
        ),
        migrations.AlterModelOptions(
            name='user',
            options={'verbose_name': 'user', 'verbose_name_plural': 'users'},
        ),
        migrations.AlterModelManagers(
            name='service',
            managers=[
            ],
        ),
        migrations.RenameField(
            model_name='user',
            old_name='complete_name',
            new_name='password',
        ),
        migrations.RemoveField(
            model_name='service',
            name='date_joined',
        ),
        migrations.RemoveField(
            model_name='service',
            name='first_name',
        ),
        migrations.RemoveField(
            model_name='service',
            name='groups',
        ),
        migrations.RemoveField(
            model_name='service',
            name='id',
        ),
        migrations.RemoveField(
            model_name='service',
            name='is_active',
        ),
        migrations.RemoveField(
            model_name='service',
            name='is_staff',
        ),
        migrations.RemoveField(
            model_name='service',
            name='is_superuser',
        ),
        migrations.RemoveField(
            model_name='service',
            name='last_login',
        ),
        migrations.RemoveField(
            model_name='service',
            name='last_name',
        ),
        migrations.RemoveField(
            model_name='service',
            name='user_permissions',
        ),
        migrations.RemoveField(
            model_name='service',
            name='username',
        ),
        migrations.RemoveField(
            model_name='user',
            name='apartment',
        ),
        migrations.RemoveField(
            model_name='user',
            name='block',
        ),
        migrations.RemoveField(
            model_name='user',
            name='cpf',
        ),
        migrations.RemoveField(
            model_name='user',
            name='phone',
        ),
        migrations.RemoveField(
            model_name='user',
            name='voice_data',
        ),
        migrations.AddField(
            model_name='service',
            name='complete_name',
            field=models.CharField(default=1, max_length=80),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='service',
            name='user',
            field=models.OneToOneField(default=1, on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='user',
            name='date_joined',
            field=models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined'),
        ),
        migrations.AddField(
            model_name='user',
            name='first_name',
            field=models.CharField(blank=True, max_length=30, verbose_name='first name'),
        ),
        migrations.AddField(
            model_name='user',
            name='groups',
            field=models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups'),
        ),
        migrations.AddField(
            model_name='user',
            name='is_active',
            field=models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active'),
        ),
        migrations.AddField(
            model_name='user',
            name='is_admin',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='user',
            name='is_resident',
            field=models.BooleanField(default=False, verbose_name='student status'),
        ),
        migrations.AddField(
            model_name='user',
            name='is_service',
            field=models.BooleanField(default=False, verbose_name='visitor status'),
        ),
        migrations.AddField(
            model_name='user',
            name='is_staff',
            field=models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status'),
        ),
        migrations.AddField(
            model_name='user',
            name='is_superuser',
            field=models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status'),
        ),
        migrations.AddField(
            model_name='user',
            name='last_login',
            field=models.DateTimeField(blank=True, null=True, verbose_name='last login'),
        ),
        migrations.AddField(
            model_name='user',
            name='last_name',
            field=models.CharField(blank=True, max_length=150, verbose_name='last name'),
        ),
        migrations.AddField(
            model_name='user',
            name='user_permissions',
            field=models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions'),
        ),
        migrations.AddField(
            model_name='user',
            name='username',
            field=models.CharField(default=11, max_length=40),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='service',
            name='email',
            field=models.CharField(max_length=90),
        ),
        migrations.AlterField(
            model_name='user',
            name='email',
            field=models.CharField(max_length=40, unique=True),
        ),
        migrations.AlterField(
            model_name='visitor',
            name='owner',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='accounts.Resident'),
        ),
    ]
