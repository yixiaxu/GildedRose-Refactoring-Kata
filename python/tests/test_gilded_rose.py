# -*- coding: utf-8 -*-
import unittest

from gilded_rose import Item, GildedRose


class GildedRoseTest(unittest.TestCase):
    def test_foo(self):
        items = [Item("foo", 0, 0)]
        gilded_rose = GildedRose(items)
        gilded_rose.update_quality()
        self.assertEqual("foo", items[0].name) # 这里我把 "fixme" 改成了 "foo"，不然原本的测试也会报错

    def test_conjured_item_decregrades_twice_as_fast(self):
        items = [Item("Conjured Mana Cake", 3, 6)]
        gilded_rose = GildedRose(items)
        gilded_rose.update_quality()
        self.assertEqual(4, items[0].quality)

    def test_conjured_item_past_sell_in_date_decregrades_four_times_as_fast(self):
        items = [Item("Conjured Mana Cake", 0, 10)]
        gilded_rose = GildedRose(items)
        gilded_rose.update_quality()
        self.assertEqual(6, items[0].quality)

    def test_conjured_item_quality_never_negative(self):
        items = [Item("Conjured Mana Cake", 3, 1)]
        gilded_rose = GildedRose(items)
        gilded_rose.update_quality()
        self.assertEqual(0, items[0].quality)

    def test_conjured_item_sell_in_decreases(self):
        items = [Item("Conjured Mana Cake", 3, 6)]
        gilded_rose = GildedRose(items)
        gilded_rose.update_quality()
        self.assertEqual(2, items[0].sell_in)

        
if __name__ == '__main__':
    unittest.main()