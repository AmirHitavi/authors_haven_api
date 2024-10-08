from django.contrib import admin

from .models import Response

# Register your models here.


@admin.register(Response)
class ResponseRating(admin.ModelAdmin):
    list_display = ["id", "user", "article", "parent", "created_at"]
    list_display_links = ["id", "article", "user"]
