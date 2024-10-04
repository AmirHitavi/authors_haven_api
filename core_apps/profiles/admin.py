from django.contrib import admin

from .models import Profile

# Register your models here.


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ["pk_id", "id", "user", "gender", "phone_number", "country", "city"]
    list_display_links = [
        "pk_id",
        "id",
        "user",
    ]

    list_filter = ["pk_id", "id"]
