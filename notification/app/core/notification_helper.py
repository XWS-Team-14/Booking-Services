from app.models.notification import Notification
from app.models.notification_type import NotificationType


def generate(notification: Notification, notification_type: str):
    if notification_type == 'host-new-reservation':
        notification.title = f'{notification.accommodation.name}: New reservation'
        notification.content = f'{notification.sender.name} has created a reservation for your accommodation {notification.accommodation.name}.'

    elif notification_type == 'host-reservation-cancelled':
        notification.title = f'{notification.accommodation.name}: Reservation cancelled'
        notification.content = f'{notification.sender.name} has cancelled the reservation for your accommodation {notification.accommodation.name}.'

    elif notification_type == 'host-new-review':
        notification.title = 'New rating'
        notification.content = f'You have received a new rating. Check it out!'

    elif notification_type == 'host-accommodation-new-review':
        notification.title = f'{notification.accommodation.name}: New review'
        notification.content = f'Your accommodation {notification.accommodation.name} has received a new rating. Check it out!'

    elif notification_type == 'featured-host-lost':
        notification.title = 'Featured status lost'
        notification.content = 'You no longer have the status of a featured host.'

    elif notification_type == 'featured-host-gained':
        notification.title = 'You are a featured host!'
        notification.content = 'Due to your remarkable results, you have received the status of a featured host.'

    elif notification_type == 'host-reply-approved':
        notification.title = 'Reservation approved!'
        notification.content = f'{notification.sender.name} has approved your reservation at {notification.accommodation.name}!'

    elif notification_type == 'host-reply-denied':
        notification.title = 'Reservation denied'
        notification.content = f'Unfortunately, {notification.sender.name} did not approve your reservation at {notification.accommodation.name}.'

    else:
        notification.title = ''
        notification.content = ''

    return notification


def get_type(input: str):
    if input == "featured-host-lost" or input == "featured-host-gained":
        return 'host-featured-update'
    elif input == "host-reply-approved" or input == "host-reply-denied":
        return 'guest-reservation-update'
    else:
        return input
