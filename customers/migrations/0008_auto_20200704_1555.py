# Generated by Django 3.0.7 on 2020-07-04 10:10

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('customers', '0007_auto_20200310_1402'),
    ]

    operations = [
        migrations.RenameField(
            model_name='customer',
            old_name='created_at',
            new_name='date_created',
        ),
    ]
