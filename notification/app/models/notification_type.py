from enum import Enum


class NotificationType(str, Enum):
    HOST_NEW_RESERVATION = "host-new-reservation",
    HOST_RESERVATION_CANCELLED = "host-reservation-cancelled",
    HOST_NEW_REVIEW = "host-new-review",
    HOST_ACCOMMODATION_NEW_REVIEW = "host-accommodation-new-review",
    HOST_FEATURED_UPDATE = "host-featured-update",
    GUEST_RESERVATION_UPDATE = "guest-reservation-update"
