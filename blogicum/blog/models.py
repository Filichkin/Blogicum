from django.db import models
from django.contrib.auth import get_user_model

from core.models import PublishedModel
from .constants import MAX_LENGTH


User = get_user_model()


class Location(PublishedModel):
    """Географическая метка."""

    name = models.CharField(
        max_length=MAX_LENGTH,
        verbose_name='Название места'
    )

    class Meta:
        verbose_name = 'местоположение'
        verbose_name_plural = 'Местоположения'

    def __str__(self) -> str:
        name = str(self.name)
        return name


class Category(PublishedModel):
    """Тематическая категория."""

    title = models.CharField(
        max_length=MAX_LENGTH,
        verbose_name='Заголовок'
    )
    description = models.TextField(
        verbose_name='Описание'
    )
    slug = models.SlugField(
        max_length=MAX_LENGTH,
        unique=True,
        verbose_name='Идентификатор',
        help_text='Идентификатор страницы для URL; '
                  'разрешены символы латиницы, цифры, дефис и подчёркивание.'
    )

    class Meta:
        verbose_name = 'категория'
        verbose_name_plural = 'Категории'

    def __str__(self) -> str:
        title = str(self.title)
        return title


class Post(PublishedModel):
    """Публикация."""

    title = models.CharField(
        max_length=MAX_LENGTH,
        verbose_name='Заголовок'
    )
    text = models.TextField(
        verbose_name='Текст'
    )
    pub_date = models.DateTimeField(
        verbose_name='Дата и время публикации',
        help_text='Если установить дату и время в будущем — '
                  'можно делать отложенные публикации.'
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Автор публикации',
        related_name='posts'
    )
    location = models.ForeignKey(
        Location,
        on_delete=models.SET_NULL,
        verbose_name='Местоположение',
        related_name='posts',
        null=True,
        blank=True
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        verbose_name='Категория',
        related_name='posts'
    )
    image = models.ImageField(
        upload_to='posts_images',
        null=True,
        blank=True,
        verbose_name='Фото к постам'
    )

    class Meta:
        ordering = ['-pub_date']
        verbose_name = 'публикация'
        verbose_name_plural = 'Публикации'

    def __str__(self) -> str:
        title = str(self.title)
        return title


class Comment(models.Model):
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        null=True,
        verbose_name='Автор комментария'
    )
    post = models.ForeignKey(
        Post,
        related_name='comments',
        on_delete=models.CASCADE,
        null=True
    )
    text = models.TextField(
        verbose_name='Текст'
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['created_at']
        verbose_name = 'комментарий'
        verbose_name_plural = 'Комментарии'

    def __str__(self):
        return self.text
