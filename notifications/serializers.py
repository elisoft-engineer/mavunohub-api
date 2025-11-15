from rest_framework import serializers

from core.serializers import EnumField
from notifications.models import Notification, NotificationStatus


class NotificationSerializer(serializers.ModelSerializer):
    status = EnumField(enum_class=NotificationStatus)
    user = serializers.ReadOnlyField(source="user.email")

    class Meta:
        model = Notification
        fields = ['id', 'message', 'user', 'status', 'created_at', 'get_humanized_time']
