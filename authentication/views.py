from django.contrib.auth import get_user_model
from rest_framework_simplejwt.views import TokenObtainPairView

from .serializers import EmailPasswordTokenObtainSerializer

User = get_user_model()


class EmailPasswordTokenObtainView(TokenObtainPairView):
    serializer_class = EmailPasswordTokenObtainSerializer
