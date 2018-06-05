# Generated by Django 2.0.3 on 2018-04-27 20:54

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Address',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('street', models.CharField(blank=True, max_length=128)),
                ('street_no', models.CharField(blank=True, max_length=16, null=True)),
                ('city', models.CharField(max_length=16)),
                ('state', models.CharField(max_length=16)),
                ('location_description', models.TextField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cat', models.CharField(max_length=100, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Founditem',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.CreateModel(
            name='Item',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('subCat', models.CharField(max_length=64)),
                ('date', models.DateField(null=True)),
                ('color', models.CharField(max_length=64)),
                ('title', models.CharField(max_length=128)),
                ('description', models.TextField()),
                ('picture', models.ImageField(blank=True, default='default.jpeg', upload_to='')),
                ('cat', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='allitems', to='lostandfound.Category')),
                ('location', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='allitems', to='lostandfound.Address')),
            ],
        ),
        migrations.CreateModel(
            name='Lostitem',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('item', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='lostandfound.Item')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('phone', models.CharField(blank=True, max_length=10)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='founditem',
            name='item',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='lostandfound.Item'),
        ),
        migrations.AddField(
            model_name='founditem',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
