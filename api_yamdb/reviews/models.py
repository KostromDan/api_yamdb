import uuid
from datetime import date

from api_yamdb.settings import DEFAULT_ROLE

from django.contrib.auth.models import AbstractUser
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.db.models import (
    CharField, CheckConstraint, Q, TextField, UniqueConstraint)


class User(AbstractUser):
    role = CharField(
        'Роль',
        max_length=10,
        blank=False,
        default=DEFAULT_ROLE
    )
    bio = TextField(
        'Биография',
        blank=True,
    )
    confirmation_code = models.UUIDField('Код подтверждения',
                                         default=uuid.uuid4)


class Genre(models.Model):
    name = models.CharField(max_length=256, verbose_name='Название')
    slug = models.SlugField(
        max_length=50,
        unique=True
    )

    def __str__(self):
        return self.name


class Category(models.Model):
    name = models.CharField(max_length=256, verbose_name='Название')
    slug = models.SlugField(
        max_length=50,
        unique=True
    )

    def __str__(self):
        return self.name


class Title(models.Model):
    name = models.TextField(verbose_name='Название')
    year = models.IntegerField(verbose_name='Год выхода')
    description = models.TextField(
        max_length=256,
        verbose_name='Описание',
        blank=True, null=True)
    genre = models.ManyToManyField(
        'Genre',
        related_name='assigned_genre',
        verbose_name='Жанр',
        through='TitleGenre')
    category = models.ForeignKey(
        'Category',
        on_delete=models.SET_NULL,
        blank=True, null=True,
        related_name='titles',
        verbose_name='Категория'
    )

    class Meta:
        constraints = (
            CheckConstraint(
                check=(Q(year__lte=date.today().year)),
                name='%(app_label)s_%(class)s_year__less__today'
            ),
        )

    def __str__(self):
        return self.name[:15]


class TitleGenre(models.Model):
    title_id = models.ForeignKey(Title, on_delete=models.CASCADE)
    genre_id = models.ForeignKey(Genre, on_delete=models.CASCADE)

    class Meta:
        constraints = (
            UniqueConstraint(
                fields=['title_id', 'genre_id'],
                name='%(app_label)s_%(class)s_genre__title__unique'
            ),
        )


class Review(models.Model):
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name='Произведение'
    )
    text = models.TextField(
        verbose_name='Текст',
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name='Автор'
    )
    score = models.IntegerField(
        validators=[
            MinValueValidator(1, 'Integer value from 1 to 10'),
            MaxValueValidator(10, 'Integer value from 1 to 10')
        ],
        verbose_name='Оценка'
    )
    pub_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата публикации'
    )

    class Meta:
        ordering = ('-pub_date',)
        constraints = [
            models.UniqueConstraint(
                fields=('author', 'title',),
                name='unique review'
            )
        ]
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'


class Comment(models.Model):
    text = models.TextField(
        verbose_name='Текст',
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='Автор'
    )
    review = models.ForeignKey(
        Review,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='Отзыв'
    )
    pub_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата публикации'
    )

    class Meta:
        ordering = ('-pub_date',)
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'
