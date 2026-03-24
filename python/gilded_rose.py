# -*- coding: utf-8 -*-
from abc import ABC, abstractmethod


class Item:
    def __init__(self, name, sell_in, quality):
        self.name = name
        self.sell_in = sell_in
        self.quality = quality

    def __repr__(self):
        return "%s, %s, %s" % (self.name, self.sell_in, self.quality)


class UpdateStrategy(ABC):
    """Abstract base strategy for item updates."""
    MIN_QUALITY = 0
    MAX_QUALITY = 50

    def clamp_quality(self, value, min_q=None, max_q=None):
        """Keep quality within valid bounds."""
        if min_q is None:
            min_q = self.MIN_QUALITY
        if max_q is None:
            max_q = self.MAX_QUALITY
        return max(min_q, min(max_q, value))

    @abstractmethod
    def update(self, item):
        """Update item based on strategy. Subclasses must implement."""
        pass


class DefaultStrategy(UpdateStrategy):
    """Default strategy for normal items that degrade in quality."""
    NORMAL_DECREASE = 1
    EXPIRED_DECREASE = 2

    def update(self, item):
        item.sell_in -= 1
        decrease = self.EXPIRED_DECREASE if item.sell_in < 0 else self.NORMAL_DECREASE
        item.quality = self.clamp_quality(item.quality - decrease)


class AgedBrieStrategy(UpdateStrategy):
    """Aged Brie increases in quality over time."""
    NORMAL_INCREASE = 1
    EXPIRED_INCREASE = 2

    def update(self, item):
        item.sell_in -= 1
        increase = self.EXPIRED_INCREASE if item.sell_in < 0 else self.NORMAL_INCREASE
        item.quality = self.clamp_quality(item.quality + increase)


class SulfurasStrategy(UpdateStrategy):
    def update(self, item):
        pass


class BackstagePassStrategy(UpdateStrategy):
    """Backstage passes increase in value as the concert date approaches."""
    DAYS_TO_EXPIRE = 0
    INCREASE_VERY_CLOSE = 3   # Less than 5 days
    INCREASE_CLOSE = 2         # 5-10 days
    INCREASE_NORMAL = 1        # More than 10 days
    CRITICAL_DAYS = 5
    WARNING_DAYS = 10

    def _calculate_quality_increase(self, days_remaining):
        """Determine quality increase based on days until concert."""
        if days_remaining < self.CRITICAL_DAYS:
            return self.INCREASE_VERY_CLOSE
        elif days_remaining < self.WARNING_DAYS:
            return self.INCREASE_CLOSE
        else:
            return self.INCREASE_NORMAL

    def update(self, item):
        item.sell_in -= 1
        if item.sell_in < self.DAYS_TO_EXPIRE:
            # Concert has passed, ticket is worthless
            item.quality = self.MIN_QUALITY
        else:
            # Concert is upcoming, increase quality
            increase = self._calculate_quality_increase(item.sell_in)
            item.quality = self.clamp_quality(item.quality + increase)


class ConjuredStrategy(UpdateStrategy):
    """Conjured items degrade twice as fast as normal items."""
    NORMAL_DECREASE = 2
    EXPIRED_DECREASE = 4

    def update(self, item):
        item.sell_in -= 1
        decrease = self.EXPIRED_DECREASE if item.sell_in < 0 else self.NORMAL_DECREASE
        item.quality = self.clamp_quality(item.quality - decrease)


class StrategyFactory:
    """Factory for creating item update strategies based on item name."""
    
    # Registry of item names to strategy classes
    _STRATEGIES = {
        "Aged Brie": AgedBrieStrategy,
        "Sulfuras, Hand of Ragnaros": SulfurasStrategy,
        "Backstage passes to a TAFKAL80ETC concert": BackstagePassStrategy,
        "Conjured Mana Cake": ConjuredStrategy
    }
    
    @classmethod
    def get_strategy(cls, item_name):
        """Get the appropriate strategy for an item.
        
        Args:
            item_name: Name of the item
            
        Returns:
            An UpdateStrategy instance (default or item-specific)
        """
        strategy_class = cls._STRATEGIES.get(item_name, DefaultStrategy)
        return strategy_class()
    
    @classmethod
    def register_strategy(cls, item_name, strategy_class):
        """Register a new strategy for an item name.
        
        Allows dynamic registration of new item types without modifying
        the factory class itself.
        """
        cls._STRATEGIES[item_name] = strategy_class


class GildedRose(object):
    """Manages item inventory and updates quality based on specific rules."""
    
    def __init__(self, items):
        self.items = items
    
    def update_quality(self):
        """Update quality for all items based on their type."""
        for item in self.items:
            strategy = StrategyFactory.get_strategy(item.name)
            strategy.update(item)