__author__ = "Pinkas Matěj"
__email__ = "pinkas.matej@gmail.com"
__created__ = "10/12/2025"

"""
Project: B4B33RPH
Filename: quality.py
Directory: homeworks/spam_filter/
"""

import os
from utils import read_classification_from_file
from confmat import BinaryConfusionMatrix

def quality_score(tp, tn, fp, fn):
    return (tp + tn)/(tp+tn+(10*fp)+fn)

def compute_quality_for_corpus(corpus_dir):
    truth_file_path = os.path.join(corpus_dir, '!truth.txt')
    prediction_file_path = os.path.join(corpus_dir, '!prediction.txt')

    truth = read_classification_from_file(truth_file_path)
    prediction = read_classification_from_file(prediction_file_path)

    binary_matrix = BinaryConfusionMatrix(pos_tag='SPAM', neg_tag='OK')
    binary_matrix.compute_from_dicts(truth, prediction)

    dictionary = binary_matrix.as_dict()

    score = quality_score(dictionary['tp'], dictionary['tn'], dictionary['fp'], dictionary['fn'])

    return score


if __name__ == '__main__':
    pass
