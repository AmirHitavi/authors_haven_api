from django.contrib import admin

from .models import Bookmark

# Register your models here.


@admin.register(Bookmark)
class BookmarkAdmin(admin.ModelAdmin):
    list_display = ["id", "user", "article", "created_at"]
    list_display_links = ["id", "user", "article"]
