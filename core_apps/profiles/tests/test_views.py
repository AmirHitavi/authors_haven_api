import uuid

import pytest
from django.contrib.auth import get_user_model
from django.core import mail
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from core_apps.profiles.models import Profile
from core_apps.profiles.serializers import FollowingSerializer
from core_apps.profiles.tests.factories import ProfileFactory
from core_apps.profiles.views import ProfileDetailsAPIView

User = get_user_model()


@pytest.mark.django_db
def test_profile_list(normal_user):

    client = APIClient()
    url = reverse("all-profiles")

    response = client.get(url)
    assert response.status_code == status.HTTP_401_UNAUTHORIZED

    client.force_authenticate(user=normal_user)

    response = client.get(url)
    assert response.status_code == status.HTTP_200_OK


@pytest.mark.django_db
def test_profile_list_method_not_allowed(normal_user):

    client = APIClient()
    client.force_authenticate(user=normal_user)
    url = reverse("all-profiles")

    response = client.post(url)
    assert response.status_code == status.HTTP_405_METHOD_NOT_ALLOWED

    response = client.patch(url)
    assert response.status_code == status.HTTP_405_METHOD_NOT_ALLOWED

    response = client.put(url)
    assert response.status_code == status.HTTP_405_METHOD_NOT_ALLOWED

    response = client.delete(url)
    assert response.status_code == status.HTTP_405_METHOD_NOT_ALLOWED


@pytest.mark.django_db
def test_profile_details(user_profile):
    user = user_profile.user

    client = APIClient()
    url = reverse("my-profile")

    response = client.get(url)
    assert response.status_code == status.HTTP_401_UNAUTHORIZED

    client.force_authenticate(user=user)

    response = client.get(url)
    assert response.status_code == status.HTTP_200_OK
    assert uuid.UUID(response.data["id"]) == user_profile.id
    assert response.data["first_name"] == user.first_name
    assert response.data["last_name"] == user.last_name
    assert response.data["email"] == user.email
    assert response.data["full_name"] == user.get_full_name
    assert response.data["phone_number"] == user_profile.phone_number
    assert response.data["about_me"] == user_profile.about_me
    assert response.data["country"] == user_profile.country.name
    assert response.data["city"] == user_profile.city
    assert response.data["profile_photo"] == user_profile.profile_photo.url
    assert response.data["twitter_handle"] == user_profile.twitter_handle


@pytest.mark.django_db
def test_profile_details_queryset(user_profile):
    user = user_profile.user

    client = APIClient()
    client.force_authenticate(user=user)

    url = reverse("my-profile")
    response = client.get(url)

    view = ProfileDetailsAPIView()
    view.request = response.wsgi_request

    queryset = view.get_queryset()

    assert queryset.count() == 1
    assert user_profile in queryset
    assert queryset[0].user == user

    # Ensure that the user profile can be retrieved with select_related
    profile = queryset.get(user=user)
    assert profile.user == user


@pytest.mark.django_db
def test_profile_details_get_object(user_profile):
    user = user_profile.user

    client = APIClient()
    client.force_authenticate(user=user)

    url = reverse("my-profile")
    response = client.get(url)

    view = ProfileDetailsAPIView()
    view.request = response.wsgi_request

    get_object = view.get_object()

    assert get_object
    assert get_object == user_profile
    assert user == get_object.user


@pytest.mark.django_db
def test_profile_details_method_not_allowed(user_profile):
    user = user_profile.user

    client = APIClient()
    client.force_authenticate(user=user)
    url = reverse("my-profile")
    response = client.post(url)
    assert response.status_code == status.HTTP_405_METHOD_NOT_ALLOWED

    response = client.patch(url)
    assert response.status_code == status.HTTP_405_METHOD_NOT_ALLOWED

    response = client.put(url)
    assert response.status_code == status.HTTP_405_METHOD_NOT_ALLOWED

    response = client.delete(url)
    assert response.status_code == status.HTTP_405_METHOD_NOT_ALLOWED


@pytest.mark.django_db
def test_update_profile(user_profile):
    user = user_profile.user

    client = APIClient()
    client.force_authenticate(user=user)
    url = reverse("update-profile")

    response = client.get(url)
    assert response.status_code == status.HTTP_200_OK

    valid_data = {
        "gender": Profile.Gender.FEMALE,
        "country": "IR",
        "city": "Tehran",
        "about_me": "Updated about me section",
        "phone_number": "+14155552671",
    }

    response = client.patch(url, data=valid_data)
    assert response.status_code == status.HTTP_200_OK
    assert response.data["gender"] == valid_data["gender"]
    assert response.data["country"] == "Iran"
    assert response.data["city"] == valid_data["city"]
    assert response.data["about_me"] == valid_data["about_me"]
    assert response.data["phone_number"] == valid_data["phone_number"]

    invalid_data = {
        "gender": Profile.Gender.FEMALE,
        "country": "Invalid Country Code",
        "city": "Tehran",
        "about_me": "Updated about me section",
        "phone_number": "+1234567890",
    }
    response = client.patch(url, data=invalid_data)
    assert response.status_code == status.HTTP_400_BAD_REQUEST


@pytest.mark.django_db
def test_update_profile_method_not_allowed(user_profile):
    user = user_profile.user

    client = APIClient()
    client.force_authenticate(user=user)

    url = reverse("update-profile")

    response = client.put(url)
    assert response.status_code == status.HTTP_405_METHOD_NOT_ALLOWED

    response = client.post(url)
    assert response.status_code == status.HTTP_405_METHOD_NOT_ALLOWED

    response = client.delete(url)
    assert response.status_code == status.HTTP_405_METHOD_NOT_ALLOWED


@pytest.mark.django_db
def test_follower_list(user_profile):
    user = user_profile.user

    # add some followers to user_profile
    for _ in range(10):
        profile = ProfileFactory()
        user_profile.followers.add(profile)

    client = APIClient()
    url = reverse("followers")

    response = client.get(url)
    assert response.status_code == status.HTTP_401_UNAUTHORIZED

    client.force_authenticate(user=user)

    response = client.get(url)
    assert response.status_code == status.HTTP_200_OK
    assert (
        response.data["followers"]
        == FollowingSerializer(user_profile.followers.all(), many=True).data
    )
    assert response.data["followers_count"] == user_profile.followers.count()


@pytest.mark.django_db
def test_follower_list_without_followers(user_profile):
    user = user_profile.user

    client = APIClient()
    url = reverse("followers")

    response = client.get(url)
    assert response.status_code == status.HTTP_401_UNAUTHORIZED

    client.force_authenticate(user=user)

    response = client.get(url)
    assert response.status_code == status.HTTP_200_OK
    assert response.data["followers"] == []
    assert response.data["followers_count"] == 0


@pytest.mark.django_db
def test_follower_list_profile_not_found(normal_user):

    client = APIClient()
    url = reverse("followers")

    response = client.get(url)
    assert response.status_code == status.HTTP_401_UNAUTHORIZED

    client.force_authenticate(user=normal_user)

    response = client.get(url)
    assert response.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.django_db
def test_follower_list_profile_method_not_allowed(user_profile):
    user = user_profile.user

    client = APIClient()
    client.force_authenticate(user=user)

    url = reverse("followers")

    response = client.post(url)
    assert response.status_code == status.HTTP_405_METHOD_NOT_ALLOWED

    response = client.patch(url)
    assert response.status_code == status.HTTP_405_METHOD_NOT_ALLOWED

    response = client.put(url)
    assert response.status_code == status.HTTP_405_METHOD_NOT_ALLOWED

    response = client.delete(url)
    assert response.status_code == status.HTTP_405_METHOD_NOT_ALLOWED


@pytest.mark.django_db
def test_following_list(user_profile):
    user = user_profile.user

    # add some followers to user_profile
    for _ in range(10):
        profile = ProfileFactory()
        profile.followers.add(user_profile)

    client = APIClient()
    url = reverse("following")

    response = client.get(url)
    assert response.status_code == status.HTTP_401_UNAUTHORIZED

    client.force_authenticate(user=user)

    response = client.get(url)
    assert response.status_code == status.HTTP_200_OK
    assert (
        response.data["following"]
        == FollowingSerializer(user_profile.following.all(), many=True).data
    )
    assert response.data["following_counts"] == user_profile.following.count()


@pytest.mark.django_db
def test_following_list_without_followers(user_profile):
    user = user_profile.user

    client = APIClient()
    url = reverse("following")

    response = client.get(url)
    assert response.status_code == status.HTTP_401_UNAUTHORIZED

    client.force_authenticate(user=user)

    response = client.get(url)
    assert response.status_code == status.HTTP_200_OK
    assert response.data["following"] == []
    assert response.data["following_counts"] == 0


@pytest.mark.django_db
def test_following_list_profile_not_found(normal_user):

    client = APIClient()
    url = reverse("following")

    response = client.get(url)
    assert response.status_code == status.HTTP_401_UNAUTHORIZED

    client.force_authenticate(user=normal_user)

    response = client.get(url)
    assert response.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.django_db
def test_following_list_profile_method_not_allowed(user_profile):
    user = user_profile.user

    client = APIClient()
    client.force_authenticate(user=user)

    url = reverse("following")

    response = client.post(url)
    assert response.status_code == status.HTTP_405_METHOD_NOT_ALLOWED

    response = client.patch(url)
    assert response.status_code == status.HTTP_405_METHOD_NOT_ALLOWED

    response = client.put(url)
    assert response.status_code == status.HTTP_405_METHOD_NOT_ALLOWED

    response = client.delete(url)
    assert response.status_code == status.HTTP_405_METHOD_NOT_ALLOWED


@pytest.mark.django_db
def test_follow_success(user_profile):
    user = user_profile.user

    # User Profile to follow
    user_to_follow = ProfileFactory()

    client = APIClient()
    url = reverse("follow", args=[user_to_follow.user.id])

    response = client.post(url)
    assert response.status_code == status.HTTP_401_UNAUTHORIZED

    client.force_authenticate(user=user)

    response = client.post(url)
    assert response.status_code == status.HTTP_200_OK
    assert (
        response.data["message"]
        == f"You are now following {user_to_follow.user.first_name} {user_to_follow.user.last_name}"
    )
    # assert user_profile.following.filter(id=user_to_follow.id).exists()
    # assert user_to_follow.followers.filter(id=user_profile.id).exists()

    assert len(mail.outbox) == 1
    assert mail.outbox[0].subject == "A new user follows you"
    assert user_to_follow.user.email in [recipient for recipient in mail.outbox[0].to]


@pytest.mark.django_db
def test_follow_yourself(user_profile):
    user = user_profile.user

    client = APIClient()
    url = reverse("follow", args=[user_profile.user.id])

    response = client.post(url)
    assert response.status_code == status.HTTP_401_UNAUTHORIZED

    client.force_authenticate(user=user)

    response = client.post(url)
    assert response.status_code == status.HTTP_403_FORBIDDEN
    assert response.data["detail"] == "You can't follow yourself."


@pytest.mark.django_db
def test_follow_your_followers(user_profile):
    user = user_profile.user

    profile = ProfileFactory()
    user_profile.followers.add(profile)

    client = APIClient()
    url = reverse("follow", args=[profile.user.id])

    response = client.post(url)
    assert response.status_code == status.HTTP_401_UNAUTHORIZED

    client.force_authenticate(user=user)

    response = client.post(url)
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.data["detail"] == "You can't follow your followers."


@pytest.mark.django_db
def test_follow_nonexistent_user(user_profile):
    user = user_profile.user

    user_to_follow = ProfileFactory()
    user_to_follow_id = user_to_follow.user.id
    user_to_follow.delete()

    client = APIClient()
    url = reverse("follow", args=[user_to_follow_id])

    response = client.post(url)
    assert response.status_code == status.HTTP_401_UNAUTHORIZED

    client.force_authenticate(user=user)

    response = client.post(url)
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.data["detail"] == "You can't follow a profile that does not exist."


@pytest.mark.django_db
def test_follow_method_not_allowed(user_profile):
    user = user_profile.user
    client = APIClient()
    client.force_authenticate(user=user)

    # User Profile to follow
    user_to_follow = ProfileFactory()

    url = reverse("follow", args=[user_to_follow.id])

    response = client.get(url)
    assert response.status_code == status.HTTP_405_METHOD_NOT_ALLOWED

    response = client.patch(url)
    assert response.status_code == status.HTTP_405_METHOD_NOT_ALLOWED

    response = client.put(url)
    assert response.status_code == status.HTTP_405_METHOD_NOT_ALLOWED

    response = client.delete(url)
    assert response.status_code == status.HTTP_405_METHOD_NOT_ALLOWED


@pytest.mark.django_db
def test_unfollow_success(user_profile):
    user = user_profile.user

    # User Profile to unfollow
    # First follow the user.
    user_to_unfollow = ProfileFactory()
    user_profile.followers.add(user_to_unfollow)

    client = APIClient()
    url = reverse("unfollow", args=[user_to_unfollow.user.id])

    response = client.post(url)
    assert response.status_code == status.HTTP_401_UNAUTHORIZED

    client.force_authenticate(user=user)

    response = client.post(url)
    assert response.status_code == status.HTTP_200_OK
    assert (
        response.data["message"]
        == f"You have unfollowed {user_to_unfollow.user.first_name} {user_to_unfollow.user.last_name}."
    )

    assert len(mail.outbox) == 1
    assert mail.outbox[0].subject == "A new user unfollows you"
    assert user_to_unfollow.user.email in [recipient for recipient in mail.outbox[0].to]


@pytest.mark.django_db
def test_unfollow_yourself(user_profile):
    user = user_profile.user

    client = APIClient()
    url = reverse("unfollow", args=[user_profile.user.id])

    response = client.post(url)
    assert response.status_code == status.HTTP_401_UNAUTHORIZED

    client.force_authenticate(user=user)

    response = client.post(url)
    assert response.status_code == status.HTTP_403_FORBIDDEN
    assert response.data["detail"] == "You can't unfollow yourself."


@pytest.mark.django_db
def test_unfollow_not_followers(user_profile):
    user = user_profile.user

    user_to_unfollow = ProfileFactory()

    client = APIClient()
    url = reverse("unfollow", args=[user_to_unfollow.user.id])

    response = client.post(url)
    assert response.status_code == status.HTTP_401_UNAUTHORIZED

    client.force_authenticate(user=user)

    response = client.post(url)
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert (
        response.data["detail"]
        == "You can't unfollow someone who is not your follower."
    )


@pytest.mark.django_db
def test_unfollow_nonexistent_user(user_profile):
    user = user_profile.user

    user_to_unfollow = ProfileFactory()
    user_to_unfollow_id = user_to_unfollow.user.id
    user_to_unfollow.delete()

    client = APIClient()
    url = reverse("unfollow", args=[user_to_unfollow_id])

    response = client.post(url)
    assert response.status_code == status.HTTP_401_UNAUTHORIZED

    client.force_authenticate(user=user)

    response = client.post(url)
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.data["detail"] == "You can't follow a profile that does not exist."


@pytest.mark.django_db
def test_unfollow_method_not_allowed(user_profile):
    user = user_profile.user
    client = APIClient()
    client.force_authenticate(user=user)

    # User Profile to follow
    user_to_follow = ProfileFactory()

    url = reverse("unfollow", args=[user_to_follow.id])

    response = client.get(url)
    assert response.status_code == status.HTTP_405_METHOD_NOT_ALLOWED

    response = client.patch(url)
    assert response.status_code == status.HTTP_405_METHOD_NOT_ALLOWED

    response = client.put(url)
    assert response.status_code == status.HTTP_405_METHOD_NOT_ALLOWED

    response = client.delete(url)
    assert response.status_code == status.HTTP_405_METHOD_NOT_ALLOWED
