# Generated by Django 2.0.3 on 2018-04-03 21:27

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0003_auto_20180403_1528'),
    ]

    operations = [
        migrations.CreateModel(
            name='Build_dinnerplatter',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cart', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='built_dinnerplatter_in_cart', to='orders.Cart')),
                ('dinnerplattertype', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='total_built_dinnerplatter', to='orders.Dinnerplatter')),
                ('order', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='built_dinnerplatter_in_order', to='orders.Order')),
            ],
        ),
        migrations.CreateModel(
            name='Build_pasta',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cart', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='built_pasta_in_cart', to='orders.Cart')),
                ('order', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='built_pasta_in_order', to='orders.Order')),
                ('pastatype', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='total_built_pasta', to='orders.Pasta')),
            ],
        ),
        migrations.CreateModel(
            name='Build_salad',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cart', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='built_salad_in_cart', to='orders.Cart')),
                ('order', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='built_salad_in_order', to='orders.Order')),
                ('saladtype', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='total_built_salad', to='orders.Salad')),
            ],
        ),
        migrations.CreateModel(
            name='Build_subs',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cart', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='built_subs_in_cart', to='orders.Cart')),
                ('order', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='built_subs_in_order', to='orders.Order')),
                ('subtype', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='total_built_subs', to='orders.Subs')),
            ],
        ),
        migrations.CreateModel(
            name='menu',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('salade', models.OneToOneField(on_delete=django.db.models.deletion.PROTECT, to='orders.Dinnerplatter')),
            ],
        ),
        migrations.AlterField(
            model_name='build_pizza',
            name='order',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='built_pizzas_in_order', to='orders.Order'),
        ),
    ]
