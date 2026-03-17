# -*- coding: utf-8 -*-

class Item:
    def __init__(self, name, sell_in, quality):
        self.name = name
        self.sell_in = sell_in
        self.quality = quality

    def __repr__(self):
        return "%s, %s, %s" % (self.name, self.sell_in, self.quality)


class UpdateStrategy:
    def update(self, item):
        item.sell_in -= 1
        decrease = 2 if item.sell_in < 0 else 1
        item.quality = max(0, item.quality - decrease)


class AgedBrieStrategy(UpdateStrategy):
    def update(self, item):
        item.sell_in -= 1
        increase = 2 if item.sell_in < 0 else 1
        item.quality = min(50, item.quality + increase)


class SulfurasStrategy(UpdateStrategy):
    def update(self, item):
        pass


class BackstagePassStrategy(UpdateStrategy):
    def update(self, item):
        item.sell_in -= 1
        if item.sell_in < 0:
            item.quality = 0
        elif item.sell_in < 5:
            item.quality = min(50, item.quality + 3)
        elif item.sell_in < 10:
            item.quality = min(50, item.quality + 2)
        else:
            item.quality = min(50, item.quality + 1)


class ConjuredStrategy(UpdateStrategy):
    def update(self, item):
        item.sell_in -= 1
        decrease = 4 if item.sell_in < 0 else 2
        item.quality = max(0, item.quality - decrease)


class GildedRose(object):
    def __init__(self, items):
        self.items = items
        self._strategies = {
            "Aged Brie": AgedBrieStrategy(),
            "Sulfuras, Hand of Ragnaros": SulfurasStrategy(),
            "Backstage passes to a TAFKAL80ETC concert": BackstagePassStrategy(),
            "Conjured Mana Cake": ConjuredStrategy()
        }

    def update_quality(self):
        for item in self.items:
            strategy = self._strategies.get(item.name, UpdateStrategy())
            strategy.update(item)