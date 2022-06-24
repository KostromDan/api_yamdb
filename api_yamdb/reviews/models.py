from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator
from django.db import models
from django.db.models import CharField, TextField

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
