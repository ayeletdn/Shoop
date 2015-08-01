__author__ = 'ayelet'
from asyncio import Lock
from .item import ItemState


class Stock:

    def __init__(self):
        self.items = []
        self.lock = Lock()

    def get_display_items(self):
        return [item for item in self.items if (item.state == ItemState.ON_DISPLAY)]

    # requires lock fo state check and set
    def fetch_item_from_display(self, item_type):
        """
        Get an item from display, if available
        :param item_type: the type of item requested
        :return: The requested item or None
        """
        item = None
        yield from self.lock.acquire()
        items = [item for item in self.items if (item.state == ItemState.ON_DISPLAY and item.type == item_type)]
        if len(items) > 0:
            item = items[0]
            item.state = ItemState.IN_CART
        self.lock.release()
        yield item

    # requires lock for id increment
    def insert_item(self, item):
        """
        Add an item to the warehouse
        :param item: the item to add
        :return: the item after added to the warehouse. Now uniquely identified
        """
        assert item.type is not None

        yield from self.lock.acquire()
        item.id = len(self.items)
        item.state = ItemState.ON_DISPLAY
        self.items.append(item)
        self.lock.release()
        yield item
