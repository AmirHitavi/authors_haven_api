from dj_rest_auth.views import PasswordResetConfirmView
from django.urls import include, path

from .views import UserRetrieveUpdateAPIView

urlpatterns = [
    path(
        "auth/",
        include(
            [
                path("user/", UserRetrieveUpdateAPIView.as_view(), name="user-details"),
                path("/", include("dj_rest_auth.urls")),
                path("registeraion/", include("dj_rest_auth.registration.urls")),
                path(
                    "password/reset/confirm/<uid64>/<token>/",
                    PasswordResetConfirmView.as_view(),
                    name="password-reset-confirmation",
                ),
            ]
        ),
    ),
]
