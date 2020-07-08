# Generated by Django 3.0.7 on 2020-07-01 08:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0018_remove_product_unit'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='unit',
            field=models.CharField(choices=[('UNIT', 'Choose Product Unit'), ('Kg', 'kg'), ('L', 'litre'), ('Pcs', 'pcs'), ('m2', 'm2'), ('m3', 'm3'), ('ml', 'ml')], default='', max_length=50),
        ),
    ]