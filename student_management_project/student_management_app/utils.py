# utils.py
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync

def notify_admin(message):
    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        'admin_notifications',  # Group name for admin notifications
        {
            'type': 'send_notification',
            'message': message
        }
    )