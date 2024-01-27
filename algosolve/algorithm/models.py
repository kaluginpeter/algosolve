from django.db import models
from django.contrib.auth import get_user_model

from pytils.translit import slugify


User = get_user_model()


class BaseModel(models.Model):
    is_published = models.BooleanField(
        default=True,
        verbose_name='Опубликовано',
        help_text='Снимите галочку, чтобы скрыть публикацию.'
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Добавлено'
    )

    class Meta:
        abstract = True


class Category(BaseModel):
    title = models.CharField(verbose_name='Название', max_length=256)
    description = models.TextField(verbose_name='Описание', max_length=10000)
    slug = models.SlugField(
        unique=True,
        blank=True,
        verbose_name='Идентификатор',
        help_text=('Идентификатор страницы для URL; '
                   'разрешены символы латиницы, цифры, дефис и подчёркивание.')

    )

    class Meta:
        verbose_name = 'категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            max_slug_length = self._meta.get_field('slug').max_length
            self.slug = slugify(self.title)[:max_slug_length]
        super().save(*args, **kwargs)



class Algorithm(BaseModel):
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        related_name='algorithms',
        null=True
    )
    title = models.CharField(verbose_name='Название', max_length=256)
    description = models.TextField(verbose_name='Описание', max_length=10000)
    theory = models.TextField(verbose_name='Принцип работы', max_length=10000)
    realization = models.TextField(verbose_name='Реализация', max_length=10000)
    example = models.TextField(verbose_name='Пример работы', max_length=10000)
    slug = models.SlugField(
        unique=True,
        blank=True,
        verbose_name='Идентификатор',
        help_text=('Идентификатор страницы для URL; '
                   'разрешены символы латиницы, цифры, дефис и подчёркивание.')

    )

    class Meta:
        verbose_name = 'алгоритм'
        verbose_name_plural = 'Алгоритмы'

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            max_slug_length = self._meta.get_field('slug').max_length
            self.slug = slugify(self.title)[:max_slug_length]
        super().save(*args, **kwargs)


class ImageAlgorithm(BaseModel):
    algorithm = models.ForeignKey(
        Algorithm,
        on_delete=models.CASCADE,
        related_name='photo_algorithm'
    )
    image = models.ImageField('Фото', blank=True, upload_to='algorithm_images')
    caption = models.TextField('Описание', blank=True)
    alt = models.CharField(max_length=255, blank=True)

    class Meta:
        verbose_name = 'фотография для алгоритма'
        verbose_name_plural = 'Фотографии для алгоритмов'

    def __str__(self):
        return f'{self.alt} - {self.algorithm.title}'


class TaskAlgorithm(models.Model):
    text = models.TextField(verbose_name='Описание задачи')
    algorithm = models.ForeignKey(
        Algorithm,
        on_delete=models.CASCADE,
        related_name='task_to_algorithm'
    )

    class Meta:
        verbose_name = 'задача для алгоритма'
        verbose_name_plural = 'задачи для алгоритмов'

    def __str__(self):
        return f'{self.algorithm.title} - {self.text[:30]}'


class ImageCategory(BaseModel):
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        related_name='images',
    )
    image = models.ImageField('Фото', blank=True, upload_to='category_images')

    class Meta:
        verbose_name = 'фотография для категории'
        verbose_name_plural = 'Фотографии для категорий'

    def __str__(self):
        return self.category.title


class UrlAlgorithm(BaseModel):
    title = models.CharField(verbose_name='Название', max_length=256)
    algorithm = models.ForeignKey(
        Algorithm,
        on_delete=models.CASCADE,
        related_name='url_to_theory_algorithm'
    )
    url = models.URLField(verbose_name='Ссылка', blank=True)

    class Meta:
        verbose_name = 'ссылка для алгоритма'
        verbose_name_plural = 'ссылки для алгоритмов'

    def __str__(self):
        return self.title

class UrlTaskAlgorithm(BaseModel):
    title = models.CharField(verbose_name='Название', max_length=256)
    algorithm = models.ForeignKey(
        Algorithm,
        on_delete=models.CASCADE,
        related_name='url_to_online_tasks'
    )
    url = models.URLField(verbose_name='Ссылка', blank=True)

    class Meta:
        verbose_name = 'ссылка на задачу для алгоритма'
        verbose_name_plural = 'ссылки на задачу для алгоритмов'

    def __str__(self):
        return self.title


class UrlCategory(BaseModel):
    title = models.CharField(verbose_name='Название', max_length=256)
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        related_name='urls',
    )
    url = models.URLField(verbose_name='Ссылка')

    class Meta:
        verbose_name = 'ссылка для категории'
        verbose_name_plural = 'ссылки для категорий'

    def __str__(self):
        return self.title


class Comment(models.Model):
    text = models.TextField(verbose_name='Комментарий')
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Автор'
    )
    algorithm = models.ForeignKey(
        Algorithm,
        on_delete=models.CASCADE,
        verbose_name='Алгоритм',
        related_name='comments'
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'комментарий'
        verbose_name_plural = 'Комментарии'
        ordering = ('created_at',)

    def __str__(self):
        return self.text
