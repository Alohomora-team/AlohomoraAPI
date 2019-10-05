# Generated by Django 2.2.5 on 2019-10-01 00:55

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0004_auto_20191001_0055'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='apartment',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='condos.Apartment'),
        ),
        migrations.AlterField(
            model_name='user',
            name='block',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='condos.Block'),
        ),
    ]