from enum import Enum


class NotificationType(Enum):
    NEW_RESERVATION = "new-reservation"
    RESERVATION_CANCELLED = "reservation-cancelled"
    NEW_HOST_RATING = "new-host-rating"
    NEW_ACCOMMODATION_RATING = "new-accommodation-rating"
    FEATURED_HOST_UPDATE = "featured-host-update"
    HOST_REPLY = "host-reply"
