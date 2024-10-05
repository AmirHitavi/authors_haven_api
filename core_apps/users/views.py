from django.contrib.auth import get_user_model
from rest_framework.generics import RetrieveUpdateAPIView
from rest_framework.permissions import IsAuthenticated

from .serializers import UserSerializer

User = get_user_model()

# Create your views here.


class UserRetrieveUpdateAPIView(RetrieveUpdateAPIView):
    """
    Concrete view for retrieving, updating a model instance.
    """

    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user

    def get_queryset(self):
        return User.objects.none()
