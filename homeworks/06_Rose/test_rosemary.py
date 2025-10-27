__author__ = "Pinkas Matěj"
__email__ = "pinkas.matej@gmail.com"
__created__ = "27/10/2025"

"""
Project: B4B33RPH
Filename: test_rosemary.py
Directory: homeworks/06_Rose/
"""

from rosemary import Item, update

# Name never change
def test_normal_item_name_change():
    item = Item("Bread", days_left=3, quality=5)
    update(item)
    return item.name == "Bread"

def test_aged_brie_name_change():
    item = Item("Aged Brie", days_left=5, quality=10)
    update(item)
    return item.name == "Aged Brie"

def test_diamond_name_change():
    item = Item("Diamond", days_left=10, quality=100)
    update(item)
    return item.name == "Diamond"

def test_tickets_name_change():
    item = Item("Tickets", days_left=11, quality=10)
    update(item)
    return item.name == "Tickets"

# Quality never smaller than 0 and greater than 50 (except diamond)
def test_normal_item_quality_not_negative():
    item = Item("Bread", days_left=3, quality=0)
    update(item)
    return item.quality == 0

def test_aged_brie_quality_never_above_50():
    item = Item("Aged Brie", days_left=5, quality=50)
    update(item)
    return item.quality == 50

def test_tickets_quality_never_above_50():
    item = Item("Tickets", days_left=5, quality=49)
    update(item)
    return item.quality == 50

# Days left and quality decreases at the end of the day
def test_normal_item_decreases_days_left():
    item = Item("Bread", days_left=3, quality=5)
    update(item)
    return item.days_left == 2

def test_normal_item_decreases_quality_by_1():
    for i in range(-10, 10):
        item = Item("Bread", days_left=3, quality=i)
        update(item)
        if (item.quality != i-1 and i>=0) or(item.quality != 0 and i<0):
            return False
    return True

def test_normal_item_days_left_can_be_negative():
    item = Item("Bread", days_left=0, quality=10)
    update(item)
    return item.days_left == -1

def test_aged_brie_days_left_decreases():
    item = Item("Aged Brie", days_left=3, quality=10)
    update(item)
    return item.days_left == 2

def test_tickets_days_left_decreases():
    item = Item("Tickets", days_left=10, quality=10)
    update(item)
    return item.days_left == 9

# Days left <= 0 decays 2x faster
def test_normal_item_quality_decreases_twice_after_expiration():
    item = Item("Bread", days_left=-1, quality=6)
    update(item)
    return item.quality == 4

def test_normal_item_quality_decreases_twice_on_expiration_day():
    item = Item("Bread", days_left=0, quality=10)
    update(item)
    return item.quality == 8

# Diamonds don't change quality and days left
def test_diamond_quality_dent_change():
    item = Item("Diamond", days_left=10, quality=100)
    update(item)
    return item.quality == 100

def test_diamond_days_left_dont_change():
    item = Item("Diamond", days_left=10, quality=100)
    update(item)
    return item.days_left == 10

# Aged Bride quality increases
def test_aged_brie_increases_quality_by_1():
    item = Item("Aged Brie", days_left=5, quality=10)
    update(item)
    return item.quality == 11

def test_aged_brie_increases_quality_by_1_negative():       # NEW
    item = Item("Aged Brie", days_left=-1, quality=10)
    update(item)
    return item.quality == 11

# Tickets more than 10 days
def test_tickets_increase_by_1_when_more_than_10_days():
    item = Item("Tickets", days_left=11, quality=10)
    update(item)
    return item.quality == 11

# Tickets 6-10 days
def test_tickets_increase_by_2_when_6_to_10_days_left():
    for i in range(6,11):
        item = Item("Tickets", days_left=i, quality=10)
        update(item)
        if item.quality != 12:
            return False
    return True

# Tickets 1-5 days
def test_tickets_increase_by_3_when_1_to_5_days_left():
    for i in range(1, 6):
        item = Item("Tickets", days_left=i, quality=10)
        update(item)
        if item.quality != 13:
            return False
    return True

# Tickets quality on event day drops to 0
def test_tickets_quality_drops_to_0_on_event_day():
    item = Item("Tickets", days_left=0, quality=10)
    update(item)
    return item.quality == 0

def test_tickets_quality_drops_to_0_after_event():
    item = Item("Tickets", days_left=-1, quality=20)
    update(item)
    return item.quality == 0


if __name__ == '__main__':
    pass
