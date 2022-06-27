from django.contrib import admin

from .models import Category, Genre, Title, User


@admin.register(Category, Genre, Title, User)
class ReviewAdmin(admin.ModelAdmin):
    pass
