# Generated by Django 2.2.5 on 2019-10-23 12:57

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Block',
            fields=[
                ('number', models.CharField(max_length=4, primary_key=True, serialize=False)),
            ],
        ),
        migrations.CreateModel(
            name='Apartment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('number', models.CharField(max_length=6)),
                ('block', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='apartments', to='condos.Block')),
            ],
            options={
                'unique_together': {('number', 'block')},
            },
        ),
    ]
