import logging

from django.contrib.auth import get_user_model

from .models import Notification

User = get_user_model()
logger = logging.getLogger(__name__)

def create_notification(user, message: str):
    if not isinstance(user, User) or not user:
        logger.warning("Invalid user provided for notification.")
        return None

    if not message:
        logger.warning("Notification message cannot be empty.")
        return None

    try:
        notification = Notification.objects.create(user=user, message=message)
        return notification
    except Exception as e:
        logger.error(f"Failed to create notification: {e}")
        return None
