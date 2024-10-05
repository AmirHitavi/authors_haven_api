from django_countries.serializer_fields import CountryField
from rest_framework import serializers

from .models import Profile


class ProfileSerializer(serializers.ModelSerializer):
    first_name = serializers.CharField(source="user.first_name")
    last_name = serializers.CharField(source="user.last_name")
    email = serializers.EmailField(source="user.email")
    full_name = serializers.SerializerMethodField(read_only=True)
    profile_photo = serializers.SerializerMethodField()
    country = CountryField(name_only=True)

    class Meta:
        model = Profile
        fields = [
            "id",
            "first_name",
            "last_name",
            "email",
            "full_name",
            "phone_number",
            "about_me",
            "gender",
            "country",
            "city",
            "profile_photo",
            "twitter_handle",
        ]

    def get_full_name(self, obj):
        return f"{obj.user.first_name.title()} {obj.user.last_name.title()}"

    def get_profile_photo(self, obj):
        return obj.profile_photo.url


class ProfileUpdateSerializer(serializers.ModelSerializer):
    country = CountryField(name_only=True)

    class Meta:
        model = Profile
        fields = [
            "gender",
            "country",
            "city",
            "profile_photo",
            "twitter_handle",
            "about_me",
            "phone_number",
        ]


class FollowingSerializer(serializers.ModelSerializer):
    first_name = serializers.CharField(source="user.first_name")
    last_name = serializers.CharField(source="user.last_name")

    class Meta:
        model = Profile
        fields = [
            "first_name",
            "last_name",
            "profile_photo",
            "about_me",
            "twitter_handle",
        ]
