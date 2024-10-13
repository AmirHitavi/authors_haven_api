import pytest
from rest_framework.exceptions import ValidationError

from core_apps.profiles.models import Profile
from core_apps.profiles.serializers import (
    FollowingSerializer,
    ProfileSerializer,
    ProfileUpdateSerializer,
)


@pytest.mark.django_db
def test_profile_serializer(user_profile):
    serializer = ProfileSerializer(user_profile)

    assert "id" in serializer.data
    assert "first_name" in serializer.data
    assert "last_name" in serializer.data
    assert "email" in serializer.data
    assert "full_name" in serializer.data
    assert "phone_number" in serializer.data
    assert "about_me" in serializer.data
    assert "gender" in serializer.data
    assert "country" in serializer.data
    assert "city" in serializer.data
    assert "profile_photo" in serializer.data
    assert "twitter_handle" in serializer.data


@pytest.mark.django_db
def test_profile_full_name(user_profile):
    serializer = ProfileSerializer(user_profile)
    assert "full_name" in serializer.data
    assert (
        serializer.data["full_name"]
        == f"{user_profile.user.first_name.title()} {user_profile.user.last_name.title()}"
    )


@pytest.mark.django_db
def test_profile_profile_photo(user_profile):
    serializer = ProfileSerializer(user_profile)
    assert "profile_photo" in serializer.data
    assert serializer.data["profile_photo"] == f"{user_profile.profile_photo.url}"


@pytest.mark.django_db
def test_update_valid_profile_serializer(user_profile):

    valid_data = {
        "gender": Profile.Gender.FEMALE,
        "country": "US",
        "city": "New York",
        "about_me": "Updated about me section",
        "phone_number": "+14155552671",
    }
    serializer = ProfileUpdateSerializer(
        data=valid_data, instance=user_profile, partial=True
    )
    serializer.is_valid()
    updated_profile = serializer.save()

    assert valid_data["gender"] == updated_profile.gender
    assert valid_data["country"] == updated_profile.country
    assert valid_data["city"] == updated_profile.city
    assert valid_data["about_me"] == updated_profile.about_me
    assert valid_data["phone_number"] == updated_profile.phone_number


@pytest.mark.django_db
def test_update_invalid_phone_number_profile_serializer(user_profile):
    invalid_data = {"phone_number": "+1234567890"}

    serializer = ProfileUpdateSerializer(
        data=invalid_data, instance=user_profile, partial=True
    )

    with pytest.raises(ValidationError):
        serializer.is_valid(raise_exception=True)


@pytest.mark.django_db
def test_update_invalid_country_code_profile_serializer(user_profile):
    invalid_data = {"country": "Invalid Country Code"}

    serializer = ProfileUpdateSerializer(
        data=invalid_data, instance=user_profile, partial=True
    )

    with pytest.raises(ValidationError):
        serializer.is_valid(raise_exception=True)


@pytest.mark.django_db
def test_following_serializer(user_profile):
    serializer = FollowingSerializer(user_profile)

    assert "first_name" in serializer.data
    assert user_profile.user.first_name == serializer.data["first_name"]
    assert "last_name" in serializer.data
    assert user_profile.user.last_name == serializer.data["last_name"]
    assert "profile_photo" in serializer.data
    assert "about_me" in serializer.data
    assert "twitter_handle" in serializer.data
