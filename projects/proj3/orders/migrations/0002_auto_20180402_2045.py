# Generated by Django 2.0.3 on 2018-04-02 20:45

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='cart',
            name='total_cost',
        ),
        migrations.RemoveField(
            model_name='cart',
            name='total_items',
        ),
    ]
