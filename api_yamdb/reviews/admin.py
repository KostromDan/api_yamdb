from django.contrib import admin

from .models import User, Genre, Category


@admin.register(User, Genre, Category)
class PostAdmin(admin.ModelAdmin):
    pass
