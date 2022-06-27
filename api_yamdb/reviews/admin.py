from django.contrib import admin

from .models import Category, Genre, User


@admin.register(User, Genre, Category)
class ReviewAdmin(admin.ModelAdmin):
    pass
