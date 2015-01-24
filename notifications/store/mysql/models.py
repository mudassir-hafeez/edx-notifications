"""
Django ORM models to support the Notification Store SQL backend
"""

from django.db import models
from model_utils.models import TimeStampedModel

from notifications.base_data import DictField

from notifications.data import (
    NotificationMessage,
)


class SQLNotificationMessage(TimeStampedModel):
    """
    Model for a notification message
    """

    payload = models.TextField()

    class Meta(object):
        """
        ORM metadata about this class
        """
        app_label = 'notifications'  # since we have this models.py file not in the root app directory
        db_table = 'notifications_notificationmessage'

    def from_data_object(self, obj):
        """
        Copy all of the values from passed in NotificationMessage
        """

        if obj.id:
            self.id = obj.id  # pylint: disable=invalid-name,attribute-defined-outside-init
        self.payload = DictField.to_json(obj.payload)

    def to_data_object(self):
        """
        Return a Notification Messave
        """

        msg = NotificationMessage(
            id=self.id,
            payload=DictField.from_json(self.payload),
        )

        return msg


class SQLNotificationUserMap(models.Model):
    """
    Information about how a Notification is tied to a targeted user, and related state (e.g. read/unread)
    """

    class Meta(object):
        """
        ORM metadata about this class
        """
        app_label = 'notifications'  # since we have this models.py file not in the root app directory
        db_table = 'notifications_notificationusermap'

    # NOTE: Be sure to add any user (the target) context we might need here
    # including email, First/Last name (to support any personalization)


class SQLNotificationType(models.Model):
    """
    Notification Type information
    """

    class Meta(object):
        """
        ORM metadata about this class
        """
        app_label = 'notifications'  # since we have this models.py file not in the root app directory
        db_table = 'notifications_notificationtype'


class SQLNotificationChannel(models.Model):
    """
    Information about how notifications are delivered, e.g. web, triggered email,
    SMS, iOS Push Notifications, etc.
    """

    class Meta(object):
        """
        ORM metadata about this class
        """
        app_label = 'notifications'  # since we have this models.py file not in the root app directory
        db_table = 'notifications_notificationchannel'


class SQLNotificationTypeRenderingProvided(models.Model):
    """
    Describes which rendering types this notification type supports, e.g. 'json', 'text', 'short-html', 'long-html'
    """

    class Meta(object):
        """
        ORM metadata about this class
        """
        app_label = 'notifications'  # since we have this models.py file not in the root app directory
        db_table = 'notifications_notificationtyperenderingprovided'


class SQLNotificationUserTypeChannelMap(models.Model):
    """
    User specific mappings of Notifications to Channel, to reflect user preferences
    """

    class Meta(object):
        """
        ORM metadata about this class
        """
        app_label = 'notifications'  # since we have this models.py file not in the root app directory
        db_table = 'notifications_notificationusertypechannelmap'


class SQLDisplayString(models.Model):
    """
    NOTE: These can be cached completely in memory
    """

    string_name = models.CharField(max_length=255, db_index=True)
    lang = models.CharField(max_length=16, db_index=True)
    string_value = models.TextField()

    class Meta(object):

        """
        ORM metadata about this class
        """
        app_label = 'notifications'  # since we have this models.py file not in the root app directory
        db_table = 'notifications_displaystring'
        unique_together = (('string_name', 'lang'),)
