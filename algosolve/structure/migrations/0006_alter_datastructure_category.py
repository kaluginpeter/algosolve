# Generated by Django 4.2.7 on 2024-01-27 19:23

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('structure', '0005_alter_datastructure_category_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='datastructure',
            name='category',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='data_structures', to='structure.categorydatestructure'),
        ),
    ]
