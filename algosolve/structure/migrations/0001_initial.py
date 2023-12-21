# Generated by Django 4.2.7 on 2023-12-17 10:59

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
            name='DataStructure',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_published', models.BooleanField(default=True, help_text='Снимите галочку, чтобы скрыть публикацию.', verbose_name='Опубликовано')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Добавлено')),
                ('title', models.CharField(max_length=256, verbose_name='Название')),
                ('description', models.TextField(max_length=10000, verbose_name='Описание')),
                ('theory', models.TextField(max_length=10000, verbose_name='Принцип работы')),
                ('realization', models.TextField(max_length=10000, verbose_name='Реализация')),
                ('example', models.TextField(max_length=10000, verbose_name='Пример работы')),
                ('slug', models.SlugField(blank=True, help_text='Идентификатор страницы для URL; разрешены символы латиницы, цифры, дефис и подчёркивание.', unique=True, verbose_name='Идентификатор')),
            ],
            options={
                'verbose_name': 'структура данных',
                'verbose_name_plural': 'Структуры данных',
            },
        ),
        migrations.CreateModel(
            name='UrlDataStructure',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_published', models.BooleanField(default=True, help_text='Снимите галочку, чтобы скрыть публикацию.', verbose_name='Опубликовано')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Добавлено')),
                ('title', models.CharField(max_length=256, verbose_name='Название')),
                ('url', models.URLField(blank=True, verbose_name='Ссылка')),
                ('data_structure', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='structure.datastructure')),
            ],
            options={
                'verbose_name': 'ссылка для структуры данных',
                'verbose_name_plural': 'ссылки для структур данных',
            },
        ),
        migrations.CreateModel(
            name='TaskDataStrucutre',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_published', models.BooleanField(default=True, help_text='Снимите галочку, чтобы скрыть публикацию.', verbose_name='Опубликовано')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Добавлено')),
                ('text', models.TextField(verbose_name='Описание задачи')),
                ('data_structure', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='structure.datastructure')),
            ],
            options={
                'verbose_name': 'задача для структуры данных',
                'verbose_name_plural': 'задачи для структур данных',
            },
        ),
        migrations.CreateModel(
            name='ImageDataStructure',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_published', models.BooleanField(default=True, help_text='Снимите галочку, чтобы скрыть публикацию.', verbose_name='Опубликовано')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Добавлено')),
                ('image', models.ImageField(blank=True, upload_to='data_structures_images', verbose_name='Фото')),
                ('caption', models.TextField(blank=True, verbose_name='Описание')),
                ('alt', models.CharField(blank=True, max_length=255)),
                ('data_structure', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='structure.datastructure')),
            ],
            options={
                'verbose_name': 'фотография для струкруры данных',
                'verbose_name_plural': 'Фотографии для структур данных',
            },
        ),
        migrations.CreateModel(
            name='CommentDataStructure',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.TextField(verbose_name='Комментарий')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Автор')),
                ('data_structure', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comments_structure_data', to='structure.datastructure', verbose_name='Структура данных')),
            ],
            options={
                'verbose_name': 'комментарий',
                'verbose_name_plural': 'Комментарии',
                'ordering': ('created_at',),
            },
        ),
    ]