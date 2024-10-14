import pytest

from core_apps.profiles.models import Profile
from core_apps.profiles.tests.factories import ProfileFactory


@pytest.mark.django_db
def test_create_profile(user_profile):
    assert user_profile.user is not None
    assert user_profile.phone_number is not None
    assert user_profile.about_me is not None
    assert user_profile.gender in [
        Profile.Gender.MALE,
        Profile.Gender.FEMALE,
        Profile.Gender.OTHER,
    ]
    assert user_profile.gender is not None
    assert user_profile.country is not None
    assert user_profile.city is not None
    assert user_profile.profile_photo is not None
    assert user_profile.twitter_handle is not None


@pytest.mark.django_db
def test_profile_str(user_profile):
    assert str(user_profile) == f"{user_profile.user.first_name}'s Profile"


@pytest.mark.django_db
def test_follow_profile(user_profile):
    profile = ProfileFactory()
    assert not user_profile.check_following(profile)

    user_profile.follow(profile)
    assert user_profile.check_following(profile)

    user_profile.unfollow(profile)
    assert not user_profile.check_following(profile)
