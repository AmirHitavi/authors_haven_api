from django.urls import include, path

from .serializers import FollowingSerializer
from .views import (FollowAPIView, FollowerListAPIView, FollowingAPIView,
                    ProfileDetailsAPIView, ProfileListAPIView, UnfollowAPIView,
                    UpdateProfileAPIView)

urlpatterns = [
    path("all/", ProfileListAPIView.as_view(), name="all-profiles"),
    path(
        "me/",
        include(
            [
                path("", ProfileDetailsAPIView.as_view(), name="my-profile"),
                path("update/", UpdateProfileAPIView.as_view(), name="update-profile"),
                path("followers/", FollowerListAPIView.as_view(), name="followers"),
                path("following/", FollowingAPIView.as_view(), name="following"),
            ]
        ),
    ),
    path("<uuid:user_id>/follow/", FollowAPIView.as_view(), name="follow"),
    path("<uuid:user_id>/unfollow/", UnfollowAPIView.as_view(), name="unfollow"),
]
