# Generated by Django 2.2.5 on 2019-09-20 23:57

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('condos', '0004_auto_20190920_2352'),
    ]

    operations = [
        migrations.RenameField(
            model_name='apartment',
            old_name='owners',
            new_name='owner',
        ),
    ]
