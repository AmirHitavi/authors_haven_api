from django.contrib import admin

from .models import Article, ArticleView, Clap

# Register your models here.


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = [
        "pk_id",
        "slug",
        "author",
        "title",
        "created_at",
        "updated_at",
    ]
    list_display_links = ["pk_id", "slug", "author"]
    list_filter = [
        "created_at",
        "updated_at",
    ]
    search_fields = ["title", "slug", "tags"]
    ordering = ["-created_at", "-updated_at"]


@admin.register(ArticleView)
class ArticleViewAdmin(admin.ModelAdmin):
    list_display = ["pk_id", "article", "user", "viewer_ip"]
    list_display_links = ["pk_id", "article"]
    list_filter = ["created_at", "updated_at"]
    search_fields = ["article", "user", "viewer_ip"]
    ordering = ["-created_at", "-updated_at"]


@admin.register(Clap)
class ClapAdmin(admin.ModelAdmin):
    list_display = ["pk_id", "article", "user", "created_at", "updated_at"]
    list_display_links = ["pk_id", "article", "user"]
    list_filter = ["created_at", "updated_at"]
    search_fields = [
        "article",
        "user",
    ]
    ordering = ["-created_at", "-updated_at"]
