from django.db import models
from django.contrib.auth import get_user_model


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
        verbose_name='Идентификатор',
        help_text=('Идентификатор страницы для URL; '
                   'разрешены символы латиницы, цифры, дефис и подчёркивание.')

    )

    class Meta:
        verbose_name = 'категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.title


class Algorithm(BaseModel):
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        null=True
    )
    title = models.CharField(verbose_name='Название', max_length=256)
    description = models.TextField(verbose_name='Описание', max_length=10000)
    theory = models.TextField(verbose_name='Принцип работы', max_length=10000)
    realization = models.TextField(verbose_name='Реализация', max_length=10000)
    example = models.TextField(verbose_name='Пример работы', max_length=10000)
    url = models.URLField('Ссылка')

    class Meta:
        verbose_name = 'алгоритм'
        verbose_name_plural = 'Алгоритмы'

    def __str__(self):
        return self.title


class ImageAlgorithm(BaseModel):
    algorithm = models.ForeignKey(
        Algorithm,
        on_delete=models.CASCADE
    )
    image = models.ImageField('Фото', blank=True, upload_to='algorithm_images')

    class Meta:
        verbose_name = 'фотография'
        verbose_name_plural = 'Фотографии'

    def __str__(self):
        return self.algorithm.title


class ImageCategory(BaseModel):
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE
    )
    image = models.ImageField('Фото', blank=True, upload_to='category_images')

    class Meta:
        verbose_name = 'фотография'
        verbose_name_plural = 'Фотографии'

    def __str__(self):
        return self.category.title


class Comment(BaseModel):
    text = models.TextField(verbose_name='Комментарий', max_length=1000)
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Автор'
    )
    algorithm = models.ForeignKey(
        Algorithm,
        on_delete=models.CASCADE,
        verbose_name='Алгоритм'
    )

    class Meta:
        verbose_name = 'комментарий'
        verbose_name_plural = 'Комментарии'
        ordering = ('created_at',)

    def __str__(self):
        return self.text
