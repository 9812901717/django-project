# Generated by Django 3.0.8 on 2020-12-18 16:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('customers', '0004_auto_20201215_1917'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customer',
            name='date_created',
            field=models.DateField(max_length=50),
        ),
    ]
