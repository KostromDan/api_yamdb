from django.contrib.auth.models import AbstractUser
from django.db.models import CharField, TextField


class User(AbstractUser):
    USER = 'USR'
    MODERATOR = 'MOD'
    ADMIN = 'ADM'
    ROLE_CHOICES = [
        (USER, 'user'),
        (MODERATOR, 'moderator'),
        (ADMIN, 'admin'),
    ]
    role = CharField(
        verbose_name='Роль',
        max_length=3,
        choices=ROLE_CHOICES,
        default=USER,
    )
    bio = TextField(
        verbose_name='Биография',
        blank=True,
    )
    confirmation_code = TextField(blank=True)
