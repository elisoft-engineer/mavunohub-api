from django.conf import settings
from django.shortcuts import get_object_or_404
from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import extend_schema, OpenApiParameter
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from accounts.models import User, UserRole
from authentication.permissions import IsSelfOrStaff, IsStaff
from notifications.utils import create_notification

from .serializers import  UserSerializer, UserCreateSerializer, UserUpdateSerializer


class UserList(APIView):
    """
    Endpoint to handle both fetching all users as well as creating a new user.
    """

    allowed_methods = ['GET', 'POST']
    
    def get_permissions(self):
        if self.request.method == 'POST':
            return [AllowAny()]
        return [IsAuthenticated(), IsStaff()]
    
    def get_serializer_class(self):
        if self.request.method == 'POST':
            return UserCreateSerializer
        return UserSerializer

    @extend_schema(
        parameters=[
            OpenApiParameter(
                name="active",
                type=OpenApiTypes.BOOL,
                required=False,
                description="Filter users by their active status (true/false)"
            ),
            OpenApiParameter(
                name="role",
                type=OpenApiTypes.STR,
                required=False,
                description=f"Filter users by role. Options: {', '.join([role.value for role in UserRole])}"
            ),
        ]
    )
    def get(self, request):
        """
        Handle GET request to fetch all users.
        """

        active = request.query_params.get('active', None)
        role = request.query_params.get('role', None)

        users = User.objects.all()

        # Filter by active status if provided
        if active is not None:
            active_bool = active.lower() in ["true", "1", "yes"]
            users = users.filter(is_active=active_bool)

        # Filter by role if provided
        if role is not None and role in [choice.value for choice in UserRole]:
            users = users.filter(role=UserRole(role))

        serializer = self.get_serializer_class()(users, many=True)
        return Response(serializer.data, status.HTTP_200_OK)
    
    def post(self, request):
        """
        Create a user
        """
        serializer = self.get_serializer_class()(
            data=request.data, context={"request": request, "region_code": settings.REGION_CODE}
        )
        if serializer.is_valid():
            user = serializer.save()
            create_notification(user, "Welcome to MavunoHub!")
            return Response(serializer.data, status.HTTP_201_CREATED)
        return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)



class UserDetail(APIView):
    """
    Endpoints for common user CRUD activities
    """
    allowed_methods = ['GET', 'PUT', 'PATCH', 'DELETE']

    def get_permissions(self):
        if self.request.method == 'PATCH':
            return [IsAuthenticated(), IsStaff()]
        return [IsAuthenticated(), IsSelfOrStaff()]
    
    def get_serializer_class(self):
        if self.request.method == 'GET':
            return UserSerializer
        elif self.request.method == 'PUT':
            return UserUpdateSerializer
        return None

    def get_object(self, pk):
        obj = get_object_or_404(User, pk=pk)
        self.check_object_permissions(self.request, obj)
        return obj
    
    def get(self, request, pk):
        """
        Get the details of a user
        """
        user = self.get_object(pk)
        serializer = self.get_serializer_class()(user)
        return Response(serializer.data)

    def put(self, request, pk):
        """
        Update the details of a user
        """
        user = self.get_object(pk)
        serializer = self.get_serializer_class()(
            user, data=request.data, context={"request": request, "region_code": settings.REGION_CODE}, partial=True
        )
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)

    def patch(self, request, pk):
        """
        Activate or deactivate a user
        """
        user = self.get_object(pk)
        user.is_active = not user.is_active
        user.save()
        return Response(
            {"detail": f"User has been {'activated' if user.is_active else 'deactivated'} successfully"},
            status.HTTP_400_BAD_REQUEST
        )

    def delete(self, request, pk):
        """
        Delete a user.
        """
        user = self.get_object(pk)
        user.delete()
        return Response({"detail": "User deleted successfully"}, status.HTTP_204_NO_CONTENT)
