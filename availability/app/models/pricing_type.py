from enum import Enum


class PricingTypeEnum(str, Enum):
    room = 'Per accomodation unit'
    guest = 'Per guest'