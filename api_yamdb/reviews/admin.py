from django.contrib import admin

from .models import Category, Genre, Title, User


@admin.register(User, Genre, Category, Title)
class PostAdmin(admin.ModelAdmin):
    pass
