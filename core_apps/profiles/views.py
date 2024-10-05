# TODO: change this in production
from mailcap import subst

from django.core.mail import send_mail
from rest_framework import generics, status
from rest_framework.exceptions import NotFound
from rest_framework.parsers import MultiPartParser
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from config.settings.local import DEFAULT_FROM_EMAIL

from .exceptions import (CantFollowYourFollower, CantFollowYourself,
                         CantUnfollowNotYourFollower, CantUnfollowYourself)
from .models import Profile
from .pagination import ProfilePagination
from .renderers import ProfileJSONRenderer, ProfilesJSONRenderer
from .serializers import (FollowingSerializer, ProfileSerializer,
                          ProfileUpdateSerializer)


class ProfileListAPIView(generics.ListAPIView):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    renderer_classes = [ProfilesJSONRenderer]
    pagination_class = ProfilePagination


class ProfileDetailsAPIView(generics.RetrieveAPIView):
    serializer_class = ProfileSerializer
    renderer_classes = [ProfileJSONRenderer]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Profile.objects.select_related("user")

    def get_object(self):
        user = self.request.user
        return self.get_queryset().get(user=user)


class UpdateProfileAPIView(generics.RetrieveAPIView):
    serializer_class = ProfileUpdateSerializer
    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser]
    renderer_classes = [ProfileJSONRenderer]

    def get_object(self):
        return self.request.user.profile

    def patch(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = ProfileUpdateSerializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)


class FollowerListAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        try:
            profile = Profile.objects.get(user__id=request.user.id)
            follower_profiles = profile.followers.all()
            serializer = FollowingSerializer(follower_profiles, many=True)
            formatted_response = {
                "status_code": status.HTTP_200_OK,
                "followers_count": follower_profiles.count(),
                "followers": serializer.data,
            }
            return Response(formatted_response, status=status.HTTP_200_OK)
        except Profile.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)


class FollowingAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        try:
            profile = Profile.objects.get(user__id=request.user.id)
            following_profiles = profile.following.all()
            following_users = [profile.user for profile in following_profiles]
            serializer = FollowingSerializer(following_users, many=True)
            formatted_response = {
                "status_code": status.HTTP_200_OK,
                "following_counts": following_profiles.count(),
                "following": serializer.data,
            }
            return Response(formatted_response, status=status.HTTP_200_OK)
        except Profile.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)


class FollowAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, following_id, format=None):
        try:
            follower_profile = request.user.profile
            following_profile = Profile.objects.get(user__id=following_id)

            if follower_profile == following_profile:
                raise CantFollowYourself()

            if follower_profile.check_following(following_profile):
                raise CantFollowYourFollower()

            follower_profile.follow(following_profile)

            # Send notification email about new follow
            subject = "A new user follows you"
            message = f"Hi there, {following_profile.user.first_name}, the user {following_profile.user.full_name} now follows you"
            recipient_list = [following_profile.user.email]
            send_mail(
                subject=subject,
                message=message,
                from_email=DEFAULT_FROM_EMAIL,
                recipient_list=recipient_list,
                fail_silently=True,
            )

            formatted_response = {
                "status_code": status.HTTP_200_OK,
                "message": f"Now, You're following {following_profile.user.full_name}",
            }

            return Response(formatted_response, status_code=status.HTTP_200_OK)
        except Profile.DoesNotExist:
            return NotFound("You can't follow a profile that does not exist.")


class UnfollowAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, following_id, format=None):
        try:
            follower_profile = request.user.profile
            following_profile = Profile.objects.get(user__id=following_id)

            if follower_profile == following_profile:
                raise CantUnfollowYourself()

            if not follower_profile.check_following(following_profile):
                raise CantUnfollowNotYourFollower()

            follower_profile.unfollow(following_profile)

            # Send notification email about new unfollow
            subject = "A new user unfollows you"
            message = f"Hi there, {following_profile.user.first_name}, the user {following_profile.user.full_name} now unfollows you"
            recipient_list = [following_profile.user.email]
            send_mail(
                subject=subject,
                message=message,
                from_email=DEFAULT_FROM_EMAIL,
                recipient_list=recipient_list,
                fail_silently=True,
            )

            formatted_response = {
                "status_code": status.HTTP_200_OK,
                "message": f"You have unfollowed {follower_profile.user.full_name}",
            }
            return Response(formatted_response, status=status.HTTP_200_OK)

        except Profile.DoesNotExist:
            return NotFound("You can't unfollow a profile that does not exist.")
