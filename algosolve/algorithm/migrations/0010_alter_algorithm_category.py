# Generated by Django 4.2.7 on 2023-12-24 10:44

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('algorithm', '0009_urltaskalgorithm'),
    ]

    operations = [
        migrations.AlterField(
            model_name='algorithm',
            name='category',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='algorithm.category'),
        ),
    ]