# Generated by Django 3.0.7 on 2020-06-21 09:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('registers', '0006_auto_20200621_1458'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='lname',
            field=models.CharField(max_length=100, null=True),
        ),
    ]
