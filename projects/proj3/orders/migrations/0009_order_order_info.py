# Generated by Django 2.0.3 on 2018-04-06 16:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0008_build_subs_extracheese'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='order_info',
            field=models.CharField(max_length=1000, null=True),
        ),
    ]
