# Generated by Django 3.1.7 on 2021-07-18 04:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0004_order_orderitem'),
    ]

    operations = [
        migrations.AlterField(
            model_name='link',
            name='code',
            field=models.CharField(max_length=255, unique=True),
        ),
    ]
