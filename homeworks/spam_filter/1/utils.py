__author__ = "Pinkas Matěj"
__email__ = "pinkas.matej@gmail.com"
__created__ = "10/12/2025"

"""
Project: B4B33RPH
Filename: utils.py
Directory: homeworks/spam_filter/
"""

def read_classification_from_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        data_dict = {}
        for line in f:
            key, val = line.strip().split(' ')
            data_dict[key] = val

    return data_dict

if __name__ == '__main__':
    pass
