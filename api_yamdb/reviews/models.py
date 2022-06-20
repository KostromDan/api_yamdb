from django.db import models

class Genre(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(max_length=49, unique=True)  # regex constraints, validators

    def __str__(self):
        return self.name


class Title(models.Model):
    name = models.TextField()
    year = models.IntegerField()  # regex constraints, validators
    description = models.TextField(max_length=255)
    genre = models.ManyToManyField(Genre)  # think about through_fields
    category = models.ForeignKey(
        'Category',
        on_delete=models.SET_NULL,
        blank=True, null=True,
        related_name='titles'
    )

    def __str__(self):
        return self.name[:15]
# verbose name
# related_name


class Category(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(max_length=49, unique=True)  # regex constraints, validators?

    def __str__(self):
        return self.name
