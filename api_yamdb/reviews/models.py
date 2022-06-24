from django.contrib.auth.models import AbstractUser, UserManager
from django.core.validators import MaxValueValidator, MinValueValidator, RegexValidator
from django.db import models
from django.db.models import CharField, TextField, constraints

slug_regex_validator = RegexValidator(
    regex=r'^[-a-zA-Z0-9_]+$',
    message='Must be letters or numbers only'
)


class User(AbstractUser):
    USER = 'U'
    MODERATOR = 'M'
    ADMIN = 'A'
    ROLE_CHOICES = [
        (USER, 'user'),
        (MODERATOR, 'moderator'),
        (ADMIN, 'admin'),
    ]
    role = CharField(
        verbose_name='Роль',
        max_length=1,
        choices=ROLE_CHOICES,
        default=USER,
    )
    bio = TextField(
        verbose_name='Биография',
        blank=True,
    )
    confirmation_code = TextField(blank=True)


class Genre(models.Model):
    name = models.CharField(max_length=256)
    slug = models.SlugField(
        max_length=50,
        unique=True,
        validators=[slug_regex_validator]
    )

    def __str__(self):
        return self.name


class Title(models.Model):
    name = models.TextField()
    year = models.IntegerField()  # maybe validator r'^[-+]?\d{1,4}$'
    description = models.TextField(max_length=256)
    genre = models.ManyToManyField(
        'Genre',
        related_name='assigned_genre')  # think about through_fields
    category = models.ForeignKey(
        'Category',
        on_delete=models.SET_NULL,
        blank=True, null=True,
        related_name='titles',
        verbose_name='Категория произведения'
    )

    class Meta:
        # think about unique constraint ['genre','name']
        # constraints = (
        #     CheckConstraint(
        #         check=(Q(year__lte=date.today().year)),
        #         name='%(app_label)s_%(class)s_year__less__today'
        #     )
        # )
        pass

    def __str__(self):
        return self.name[:15]


class Category(models.Model):
    name = models.CharField(max_length=256)
    slug = models.SlugField(
        max_length=50,
        unique=True,
        validators=[slug_regex_validator]
    )

    def __str__(self):
        return self.name


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
        ordering = ['-pub_date']
        constraints = [
            models.UniqueConstraint(
                fields=['author', 'title'],
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
        ordering = ['-pub_date']
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'
