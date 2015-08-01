__author__ = 'ayelet'
import unittest
from WareHouse.stock import Stock
from WareHouse.item import Item, ItemState


class TestStock(unittest.TestCase):
    def setUp(self):
        self.stock = Stock()

    def test_get_initial_list(self):
        self.assertEqual(self.stock.get_display_items(), [], 'initial sock should be empty')

    def test_assert_item_type_on_insert(self):
        item = Item()
        with self.assertRaises(AssertionError):
            gen = self.stock.insert_item(item)
            gen.send(None)

    def test_single_insert(self):
        item = Item("macaroni")
        self.assertEqual(item.state, ItemState.UNDEFINED, 'item state should unknown')
        generator = self.stock.insert_item(item)
        returned_item = generator.send(None)

        self.assertEqual(item, returned_item, 'returned item should be the original item')
        self.assertGreater(returned_item.id, -1, 'item id should be greater than -1')
        self.assertEqual(returned_item.state, ItemState.ON_DISPLAY, 'item state should be set to on display')

    def test_get_list_increases_after_insert(self):
        item = Item("macaroni")
        gen = self.stock.insert_item(item)
        gen.send(None)

        stock_list = self.stock.get_display_items()
        self.assertEqual(len(stock_list), 1, "There should be one item on the list")

    def test_single_fetch(self):
        item = Item("macaroni")
        gen = self.stock.insert_item(item)
        gen.send(None)

        gen = self.stock.fetch_item_from_display("macaroni")
        got_item = gen.send(None)

        self.assertEqual(item, got_item, "The returned item should be the set item")
        stock = self.stock.get_display_items()
        self.assertEqual(len(stock), 0, "There should be no items left on display")

    def test_two_inserts_at_same_time(self):
        item1 = Item("macaroni")
        item2 = Item("cheese")
        gen1 = self.stock.insert_item(item2)
        gen2 = self.stock.insert_item(item1)

        stock_list = self.stock.get_display_items()
        self.assertEqual(len(stock_list), 0, "There should be no items on the list")
        gen1.send(None)
        gen2.send(None)
        stock_list = self.stock.get_display_items()
        self.assertEqual(len(stock_list), 2, "There should be two items on the list")
        self.assertGreater(item1.id, item2.id, "The second item should have been inserted before the first")

    def test_one_insert_two_fetch(self):
        item = Item("macaroni")
        gen = self.stock.insert_item(item)
        gen.send(None)

        gen1 = self.stock.fetch_item_from_display("macaroni")
        gen2 = self.stock.fetch_item_from_display("macaroni")
        stock_list = self.stock.get_display_items()
        self.assertEqual(len(stock_list), 1, "There should be one item on the list")
        returned_item = gen1.send(None)
        self.assertIsNotNone(returned_item, "got the last item")
        returned_item = gen2.send(None)
        self.assertIsNone(returned_item, "failed to get any items")
