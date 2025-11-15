from django.shortcuts import get_object_or_404
from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import extend_schema, OpenApiParameter
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from authentication.permissions import IsOwner

from .models import Notification, NotificationStatus
from .serializers import NotificationSerializer

class NotificationList(APIView):
    """
    Endpoint to handle both fetching all notifications
    """

    allowed_methods = ['GET', 'PATCH']
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        if self.request.method == 'PATCH':
            return None
        return NotificationSerializer

    @extend_schema(
        parameters=[
            OpenApiParameter(
                name="read",
                type=OpenApiTypes.BOOL,
                required=False,
                description="Filter notifications by their read status (true/false)"
            ),
        ]
    )
    def get(self, request):
        """
        Handle GET request to fetch all developers.
        """
        read = request.query_params.get('read', None)
        if read is not None:
            read = read.lower() in ['true', '1', 'yes']
            notifications = Notification.objects.filter(
                user=request.user,
                status=NotificationStatus.READ if read else NotificationStatus.UNREAD,
            )
        else:
            notifications = Notification.objects.filter(user=request.user)

        serializer = self.get_serializer_class()(notifications, many=True)
        return Response(serializer.data, status.HTTP_200_OK)

    def patch(self, request):
        """
        Handle PATCH request to mark all the notifications as read.
        """
        notifications = Notification.objects.filter(user=request.user, status=NotificationStatus.UNREAD)
        if notifications.exists():
            notifications.update(status=NotificationStatus.READ)
            return Response({'detail': 'All notifications marked as read.'}, status.HTTP_200_OK)

        return Response({'detail': 'No unread notifications to mark as read.'}, status.HTTP_204_NO_CONTENT)


class NotificationDetail(APIView):
    """
    Retrieve, update, or delete a notification instance.
    """

    allowed_methods = ['PATCH', 'DELETE']
    permission_classes =  [IsAuthenticated, IsOwner]

    def get_object(self, pk):
        obj = get_object_or_404(Notification, pk=pk)
        self.check_object_permissions(self.request, obj)
        return obj

    def patch(self, request, pk):
        notification = self.get_object(pk)
        notification.status = NotificationStatus.READ
        notification.save()
        return Response({"detail": "Notification marked as read"}, status=status.HTTP_200_OK)

    def delete(self, request, pk):
        notification = self.get_object(pk)
        notification.delete()
        return Response({"detail": "Notification deleted successfully"}, status=status.HTTP_204_NO_CONTENT)
