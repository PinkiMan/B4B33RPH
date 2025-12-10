__author__ = "Pinkas Matěj"
__email__ = "pinkas.matej@gmail.com"
__created__ = "31/10/2025"

"""
Project: B4B33RPH
Filename: find_value.py
Directory: homeworks/
"""

def value_count(data, value):
    count = 0
    for row in data:
        for item in row:
            if item == value:
                count += 1
    return count


def value_positions(data, value):
    positions = []
    for y in range(len(data)):
        for x in range(len(data[y])):
            if data[y][x] == value:
                positions.append((y, x))
    return positions

if __name__ == '__main__':
    pass
