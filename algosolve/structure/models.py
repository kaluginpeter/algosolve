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


class CategoryDateStructure(BaseModel):
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


class DataStructure(BaseModel):
    category = models.ForeignKey(
        CategoryDateStructure,
        on_delete=models.SET_NULL,
        null=True,
        related_name='data_structures'
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
        verbose_name = 'структура данных'
        verbose_name_plural = 'Структуры данных'

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            max_slug_length = self._meta.get_field('slug').max_length
            self.slug = slugify(self.title)[:max_slug_length]
        super().save(*args, **kwargs)


class ImageDataStructure(BaseModel):
    data_structure = models.ForeignKey(
        DataStructure,
        on_delete=models.CASCADE,
        related_name='photo_data_structure'
    )
    image = models.ImageField('Фото', blank=True, upload_to='data_structures_images')
    caption = models.TextField('Описание', blank=True)
    alt = models.CharField(max_length=255, blank=True)

    class Meta:
        verbose_name = 'фотография для струкруры данных'
        verbose_name_plural = 'Фотографии для структур данных'

    def __str__(self):
        return f'{self.alt} - {self.data_structure.title}'


class TaskDataStructure(BaseModel):
    text = models.TextField(verbose_name='Описание задачи')
    data_structure = models.ForeignKey(
        DataStructure,
        on_delete=models.CASCADE,
        related_name='task_to_data_structure'
    )

    class Meta:
        verbose_name = 'задача для структуры данных'
        verbose_name_plural = 'задачи для структур данных'

    def __str__(self):
        return f'{self.data_structure.title} - {self.text[:30]}'


class UrlDataStructure(BaseModel):
    title = models.CharField(verbose_name='Название', max_length=256)
    data_structure = models.ForeignKey(
        DataStructure,
        on_delete=models.CASCADE,
        related_name='url_to_theory_data_structure'
    )
    url = models.URLField(verbose_name='Ссылка', blank=True)

    class Meta:
        verbose_name = 'ссылка для структуры данных'
        verbose_name_plural = 'ссылки для структур данных'

    def __str__(self):
        return self.title

class CommentDataStructure(models.Model):
    text = models.TextField(verbose_name='Комментарий')
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Автор'
    )
    data_structure = models.ForeignKey(
        DataStructure,
        on_delete=models.CASCADE,
        verbose_name='Структура данных',
        related_name='comments'
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'комментарий'
        verbose_name_plural = 'Комментарии'
        ordering = ('created_at',)

    def __str__(self):
        return self.text