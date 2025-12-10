__author__ = "Pinkas Matěj"
__email__ = "pinkas.matej@gmail.com"
__created__ = "10/12/2025"

"""
Project: B4B33RPH
Filename: corpus.py
Directory: homeworks/spam_filter/
"""

import os

class Corpus:
    def __init__(self, directory:str):
        self.directory = directory

    def emails(self):
        file_names = os.listdir(self.directory)
        for file_name in file_names:
            if not file_name.startswith('!'):
                file_path = os.path.join(self.directory, file_name)
                with open(file_path, 'r', encoding='utf-8') as f:
                    text = f.read()
                    yield file_name, text


if __name__ == '__main__':
    pass
