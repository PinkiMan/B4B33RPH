__author__ = "Pinkas Matěj"
__email__ = "pinkas.matej@gmail.com"
__date__ = "05/12/2025"

"""
Project: B4B33RPH
Filename: texttools.py
Directory: tests/
"""

def count_rows_and_words(filename:str):
    rows_count = 0
    words_count = 0
    with open(filename, 'r') as file:
        lines = file.readlines()

        rows_count = len(lines)

        for line in lines:
            line = line.replace('\n', '')
            words = line.split(' ')
            for word in words:
                if len(word) != 0 and word != '':
                    words_count += 1

    return rows_count, words_count

if __name__ == '__main__':
    rows, words = count_rows_and_words('example.txt')
    print(rows, words)