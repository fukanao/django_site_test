# Generated by Django 4.0.1 on 2022-05-16 06:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0006_products'),
    ]

    operations = [
        migrations.AlterField(
            model_name='blog',
            name='id',
            field=models.IntegerField(primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='products',
            name='mst_id',
            field=models.IntegerField(),
        ),
        migrations.AlterField(
            model_name='products',
            name='product',
            field=models.CharField(max_length=100),
        ),
    ]