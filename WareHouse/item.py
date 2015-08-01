__author__ = 'ayelet'
from enum import Enum


class ItemState(Enum):
    UNDEFINED = 0
    ON_DISPLAY = 1
    IN_CART = 2
    SOLD = 3


class Item:

    def __init__(self, item_type=None):
        self.id = -1
        self.type = item_type
        self.state = ItemState.UNDEFINED
