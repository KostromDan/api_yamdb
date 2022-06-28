from django.contrib import admin

from .models import Category, Genre, Title, User, Review


@admin.register(Category, Genre, Title, User, Review)
class ReviewAdmin(admin.ModelAdmin):
    pass
