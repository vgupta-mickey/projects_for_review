# Generated by Django 2.0.3 on 2018-04-03 21:53

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0005_auto_20180403_2139'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='menu',
            name='dinnerplatter',
        ),
        migrations.RemoveField(
            model_name='menu',
            name='pasta',
        ),
        migrations.RemoveField(
            model_name='menu',
            name='pizza',
        ),
        migrations.RemoveField(
            model_name='menu',
            name='salad',
        ),
        migrations.RemoveField(
            model_name='menu',
            name='subs',
        ),
        migrations.DeleteModel(
            name='menu',
        ),
    ]