# Generated by Django 3.0.3 on 2020-03-07 15:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='created_at',
            field=models.DateTimeField(max_length=50, null=True),
        ),
    ]
